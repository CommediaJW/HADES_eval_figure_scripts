import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
font_size = 20
marker_list = ["o", "^", "s", "v", "*"]
color_list = ["#c18076", "#819fa6", "#3d4a55", "#d1b5ab", "#E7D3C7"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def read_data(path):
    with open(path, "r") as file:
        reader = csv.reader(file)
        name = next(reader)[0]
        heads = next(reader)
        xtile = heads[0]
        xdata = []
        heads = heads[1:]
        ydata = {}
        for head in heads:
            ydata[head] = []
        for row in reader:
            for i in range(len(row)):
                if i == 0:
                    xdata.append(int(row[i]))
                else:
                    ydata[heads[i - 1]].append(float(row[i]))
    return name, xtile, xdata, heads, ydata


def draw_figure(plt, data, yticks, xlabel=True):
    name, xtile, xdata, heads, ydata = data

    plt.set_title(name, fontsize=font_size, y=0.74, x=0.05, fontweight="bold")
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

    xticks = np.arange(0, len(xdata), 1, dtype=float)
    x_left_padding = 0.5
    x_right_padding = 0.5
    xticks += x_left_padding
    xticks = list(xticks)
    xmin = 0
    xmax = xticks[-1] + x_right_padding
    xticks = [0] + xticks + [xmax]
    plt.set_xlim(xmin, xmax)
    if xlabel:
        xlabels = [""] + xdata + [""]
    else:
        xlabels = ["" for _ in range(len(xticks))]
    plt.set_xticks(xticks, xlabels)
    # plt.set_xlabel(xtile, fontsize=font_size, y=-0.5)

    ymin, ymax, ystep = yticks
    yticks = np.arange(ymin, ymax + ystep, ystep)
    plt.set_ylim(ymin, ymax)
    plt.set_yticks(yticks)
    # plt.set_ylabel("Epoch", fontsize=font_size, x=-1)

    for it, head in enumerate(heads):
        plt.plot(
            xticks[1:-1],
            ydata[head],
            label=head,
            linestyle='-',
            color='k',
            marker=marker_list[it],
            markerfacecolor=color_list[it],
            markersize=8,
            markeredgecolor='k',
            clip_on=False,
            zorder=10 - it,
        )


if __name__ == "__main__":
    # draw_figure("data/threshold_hot_nodes_rate.csv", "figures", 1.0, 0.5)
    # read_data("data/model_dim_epoch_time_products.csv")
    plt.figure(figsize=(9, 5))
    plt.subplots_adjust(wspace=0.5, hspace=0.15)
    plt.clf()

    pd_data = read_data("data/model_dim_epoch_time_products.csv")
    draw_figure(plt.subplot(2, 1, 1), pd_data, (0, 20, 10), xlabel=False)

    pp_data = read_data("data/model_dim_epoch_time_papers.csv")
    draw_figure(plt.subplot(2, 1, 2), pp_data, (0, 120, 60), xlabel=True)

    plt.legend(
        fontsize=font_size - 2,
        edgecolor="k",
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, 2.55),
    )

    plt.xlabel("Model Hidden Dimension Size",
               fontsize=font_size,
               labelpad=8,
               fontweight="bold")
    plt.ylabel("Epoch Time (sec)",
               fontsize=font_size,
               y=1.2,
               fontweight="bold")

    save_path = "figures/model_dim_epoch_time.pdf"
    print(f"[Note]Save to {save_path}")
    plt.savefig(save_path, bbox_inches="tight")
    plt.close("all")
