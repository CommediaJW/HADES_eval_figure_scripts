import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import torch
import os

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# hatch_list = [None, "//", "\\\\", "--"]
hatch_list = [None, None, None, None]
color_list = ["#819fa6", "#c18076", "#3d4a55", "#d1b5ab"]


def read_data(path):
    data = torch.load(path).numpy()
    print(data.max())
    print(data[data > 0].min())
    return data


def plot(data, output_path, min_xlim, max_xlim, xstep, min_ylim, max_ylim,
         ystep, ylabel):
    plt.figure(figsize=(4.2, 3.5))
    plt.clf()
    # fix parameter
    font_size = 20
    plt.rcParams['font.size'] = font_size

    # plt.title("Breakdown-GraphSAGE", fontsize=font_size + 1, y=-0.3)
    plt.tick_params(
        axis="both",
        which="major",
        labelsize=font_size,
        direction="in",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    # len_xticks = int((max_xlim - min_xlim) / xstep)
    # len_yticks = int((max_ylim - min_ylim) / ystep)
    plt.xlim(min_xlim, max_xlim)

    xticks = np.arange(min_xlim, max_xlim + xstep, xstep)
    # xlabels = np.arange(min_xlim, max_xlim + xstep, xstep)
    # ylabels = np.arange(min_ylim, max_ylim + ystep, ystep)
    plt.xticks(xticks)

    num_bins = 20
    n, bins, patches = plt.hist(data,
                                bins=num_bins,
                                density=True,
                                edgecolor="k",
                                color=color_list[0],
                                zorder=10)
    bin_width = (max(bins) - min(bins)) / num_bins
    yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    ylabels = yticks
    for i in range(len(ylabels)):
        ylabels[i] = "{:.2f}".format(ylabels[i])
    yticks = ylabels / bin_width
    plt.yticks(yticks, ylabels)
    plt.ylim(min_ylim / bin_width, max_ylim / bin_width)

    # plt.ticklabel_format(style='scientific',
    #                      axis='y',
    #                      scilimits=(5, 5),
    #                      useMathText=True)
    plt.xlabel("Accessed Times", fontsize=font_size)
    if ylabel:
        plt.ylabel("Node Ratio", fontsize=font_size)

    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, min_xlim, max_xlim, xstep, min_ylim,
                max_ylim, ystep):
    data = read_data(input_path)

    plot(data, output_path, min_xlim, max_xlim, xstep, min_ylim, max_ylim,
         ystep, True)


def draw_figure2(input_path, output_path, min_xlim, max_xlim, xstep, min_ylim,
                 max_ylim, ystep):
    data = read_data(input_path)
    print(data.max())
    print(data[data > 0].min())
    plot(data, output_path, min_xlim, max_xlim, xstep, min_ylim, max_ylim,
         ystep, False)


if __name__ == "__main__":
    data = read_data("data/ogbn-products_5,10,15_presampling_heat_drop0.pt")
    plot(data, "figures/access_times_hist_products.pdf", 0, 210, 70, 0, 0.35,
         0.07, True)
    data = read_data("data/ogbn-papers100M_5,10,15_presampling_heat_drop0.pt")
    plot(data, "figures/access_times_hist_papers.pdf", 0, 1500, 500, 0, 1, 0.2,
         True)
