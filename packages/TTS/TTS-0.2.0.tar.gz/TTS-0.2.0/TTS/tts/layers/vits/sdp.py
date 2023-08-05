import math

import torch
from torch import nn
from torch.nn import functional as F

from TTS.tts.layers.vits.transforms import piecewise_rational_quadratic_transform


class LayerNorm(nn.Module):
    def __init__(self, channels, eps=1e-5):
        super().__init__()
        self.channels = channels
        self.eps = eps

        self.gamma = nn.Parameter(torch.ones(channels))
        self.beta = nn.Parameter(torch.zeros(channels))

    def forward(self, x):
        x = x.transpose(1, -1)
        x = F.layer_norm(x, (self.channels,), self.gamma, self.beta, self.eps)
        return x.transpose(1, -1)


class Log(nn.Module):
    def forward(self, x, x_mask, reverse=False, **kwargs):
        if not reverse:
            y = torch.log(torch.clamp_min(x, 1e-5)) * x_mask
            logdet = torch.sum(-y, [1, 2])
            return y, logdet
        else:
            x = torch.exp(x) * x_mask
            return x


class Flip(nn.Module):
    def forward(self, x, *args, reverse=False, **kwargs):
        x = torch.flip(x, [1])
        if not reverse:
            logdet = torch.zeros(x.size(0)).to(dtype=x.dtype, device=x.device)
            return x, logdet
        else:
            return x


class ElementwiseAffine(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.channels = channels
        self.m = nn.Parameter(torch.zeros(channels, 1))
        self.logs = nn.Parameter(torch.zeros(channels, 1))

    def forward(self, x, x_mask, reverse=False, **kwargs):
        if not reverse:
            y = self.m + torch.exp(self.logs) * x
            y = y * x_mask
            logdet = torch.sum(self.logs * x_mask, [1, 2])
            return y, logdet
        else:
            x = (x - self.m) * torch.exp(-self.logs) * x_mask
            return x


class DDSConv(nn.Module):
    """
    Dialted and Depth-Separable Convolution
    """

    def __init__(self, channels, kernel_size, n_layers, dropout_p=0.0):
        super().__init__()
        self.channels = channels
        self.kernel_size = kernel_size
        self.n_layers = n_layers
        self.dropout_p = dropout_p

        self.drop = nn.Dropout(dropout_p)
        self.convs_sep = nn.ModuleList()
        self.convs_1x1 = nn.ModuleList()
        self.norms_1 = nn.ModuleList()
        self.norms_2 = nn.ModuleList()
        for i in range(n_layers):
            dilation = kernel_size ** i
            padding = (kernel_size * dilation - dilation) // 2
            self.convs_sep.append(
                nn.Conv1d(channels, channels, kernel_size, groups=channels, dilation=dilation, padding=padding)
            )
            self.convs_1x1.append(nn.Conv1d(channels, channels, 1))
            self.norms_1.append(LayerNorm(channels))
            self.norms_2.append(LayerNorm(channels))

    def forward(self, x, x_mask, g=None):
        if g is not None:
            x = x + g
        for i in range(self.n_layers):
            y = self.convs_sep[i](x * x_mask)
            y = self.norms_1[i](y)
            y = F.gelu(y)
            y = self.convs_1x1[i](y)
            y = self.norms_2[i](y)
            y = F.gelu(y)
            y = self.drop(y)
            x = x + y
        return x * x_mask


class ConvFlow(nn.Module):
    def __init__(self, in_channels, filter_channels, kernel_size, n_layers, num_bins=10, tail_bound=5.0):
        super().__init__()
        self.in_channels = in_channels
        self.filter_channels = filter_channels
        self.kernel_size = kernel_size
        self.n_layers = n_layers
        self.num_bins = num_bins
        self.tail_bound = tail_bound
        self.half_channels = in_channels // 2

        self.pre = nn.Conv1d(self.half_channels, filter_channels, 1)
        self.convs = DDSConv(filter_channels, kernel_size, n_layers, dropout_p=0.0)
        self.proj = nn.Conv1d(filter_channels, self.half_channels * (num_bins * 3 - 1), 1)
        self.proj.weight.data.zero_()
        self.proj.bias.data.zero_()

    def forward(self, x, x_mask, g=None, reverse=False):
        x0, x1 = torch.split(x, [self.half_channels] * 2, 1)
        h = self.pre(x0)
        h = self.convs(h, x_mask, g=g)
        h = self.proj(h) * x_mask

        b, c, t = x0.shape
        h = h.reshape(b, c, -1, t).permute(0, 1, 3, 2)  # [b, cx?, t] -> [b, c, t, ?]

        unnormalized_widths = h[..., : self.num_bins] / math.sqrt(self.filter_channels)
        unnormalized_heights = h[..., self.num_bins : 2 * self.num_bins] / math.sqrt(self.filter_channels)
        unnormalized_derivatives = h[..., 2 * self.num_bins :]

        x1, logabsdet = piecewise_rational_quadratic_transform(
            x1,
            unnormalized_widths,
            unnormalized_heights,
            unnormalized_derivatives,
            inverse=reverse,
            tails="linear",
            tail_bound=self.tail_bound,
        )

        x = torch.cat([x0, x1], 1) * x_mask
        logdet = torch.sum(logabsdet * x_mask, [1, 2])
        if not reverse:
            return x, logdet
        else:
            return x


class StochasticDurationPredictor(nn.Module):
    """Stochastic duration predictor with Spline Flows.

    It applies Variational Dequantization and Variationsl Data Augmentation.

    Paper:
        SDP: https://arxiv.org/pdf/2106.06103.pdf
        Spline Flow: https://arxiv.org/abs/1906.04032

    ::
        ## Inference

        x -> TextCondEncoder() -> Flow() -> dr_hat
        noise ----------------------^

        ## Training
                                                                              |---------------------|
        x -> TextCondEncoder() -> + -> PosteriorEncoder() -> split() -> z_u, z_v -> (d - z_u) -> concat() -> Flow() -> noise
        d -> DurCondEncoder()  -> ^                                                    |
        |------------------------------------------------------------------------------|

    Args:
        in_channels (int): Number of input tensor channels.
        hidden_channels (int): Number of hidden channels.
        kernel_size (int): Kernel size of convolutional layers.
        dropout_p (float): Dropout rate.
        num_flows (int, optional): Number of flow blocks. Defaults to 4.
        cond_channels (int, optional): Number of channels of conditioning tensor. Defaults to 0.
    """

    def __init__(
        self, in_channels: int, hidden_channels: int, kernel_size: int, dropout_p: float, num_flows=4, cond_channels=0
    ):
        super().__init__()

        self.log_flow = Log()

        # posterior encoder
        self.flows = nn.ModuleList()
        self.flows.append(ElementwiseAffine(2))
        for _ in range(num_flows):
            self.flows.append(ConvFlow(2, in_channels, kernel_size, n_layers=3))
            self.flows.append(Flip())

        # condition encoder duration
        self.post_pre = nn.Conv1d(1, in_channels, 1)
        self.post_proj = nn.Conv1d(in_channels, in_channels, 1)
        self.post_convs = DDSConv(in_channels, kernel_size, n_layers=3, dropout_p=dropout_p)

        # flow layers
        self.post_flows = nn.ModuleList()
        self.post_flows.append(ElementwiseAffine(2))
        for _ in range(num_flows):
            self.post_flows.append(ConvFlow(2, in_channels, kernel_size, n_layers=3))
            self.post_flows.append(Flip())

        # condition encoder text
        self.pre = nn.Conv1d(in_channels, in_channels, 1)
        self.convs = DDSConv(in_channels, kernel_size, n_layers=3, dropout_p=dropout_p)
        self.proj = nn.Conv1d(in_channels, in_channels, 1)

        if cond_channels != 0 and cond_channels is not None:
            self.cond = nn.Conv1d(cond_channels, hidden_channels, 1)

    def forward(self, x, x_mask, dr=None, g=None, reverse=False, noise_scale=1.0):
        x = self.pre(x)
        if g is not None:
            x = x + self.cond(g)
        x = self.convs(x, x_mask)
        x = self.proj(x) * x_mask

        if not reverse:
            flows = self.flows
            assert dr is not None

            # condition encoder duration
            h_dr = self.post_pre(dr)
            h_dr = self.post_convs(h_dr, x_mask)
            h_dr = self.post_proj(h_dr) * x_mask
            e_q = torch.randint(dr.size(0), 2, dr.size(2)).to(device=x.device, dtype=x.dtype) * x_mask
            z_q = e_q

            # posterior encoder
            logdet_tot_q = 0
            for flow in self.post_flows:
                z_q, logdet_q = flow(z_q, x_mask, g=(x + h_dr))
                logdet_tot_q += logdet_q

            z_u, z1 = torch.split(z_q, [1, 1], 1)
            u = torch.sigmoid(z_u) * x_mask
            z0 = (dr - u) * x_mask

            # posterior encoder - neg log likelihood
            logdet_tot_q += torch.sum((F.logsigmoid(z_u) + F.logsigmoid(-z_u)) * x_mask, [1, 2])
            logq = torch.sum(-0.5 * (math.log(2 * math.pi) + (e_q ** 2)) * x_mask, [1, 2]) - logdet_tot_q

            logdet_tot = 0
            z0, logdet = self.log_flow(z0, x_mask)
            logdet_tot += logdet
            z = torch.cat([z0, z1], 1)
            for flow in flows:
                z, logdet = flow(z, x_mask, g=x, reverse=reverse)
                logdet_tot = logdet_tot + logdet
            nll = torch.sum(0.5 * (math.log(2 * math.pi) + (z ** 2)) * x_mask, [1, 2]) - logdet_tot
            return nll + logq  # [b]
        else:
            flows = list(reversed(self.flows))
            flows = flows[:-2] + [flows[-1]]  # remove a useless vflow
            z = torch.rand(x.size(0), 2, x.size(2)).to(device=x.device, dtype=x.dtype) * noise_scale
            for flow in flows:
                z = flow(z, x_mask, g=x, reverse=reverse)
            z0, z1 = torch.split(z, [1, 1], 1)
            logw = z0
            return logw
