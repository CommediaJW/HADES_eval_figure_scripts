import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
font_size = 20
marker_list = ["o", "^", "s", "v", "*"]
color_list = ["#c18076", "#819fa6", "#3d4a55", "#d1b5ab", "#E7D3C7"]
hatch_list = ["//", "\\\\", None, None]


def read_data(path):
    with open(path, "r") as file:
        reader = csv.reader(file)
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
    return xtile, xdata, heads, ydata


def draw_speed(plt, data, yticks, xlabel=True):
    xtile, xdata, heads, ydata = data
    name = "Converge Speedup"

    plt.set_title(name, fontsize=font_size, y=1.02, x=0.5, fontweight="bold")
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
    if yticks[-1] > ymax:
        yticks = yticks[:-1]
    plt.set_ylim(ymin, ymax)
    plt.set_yticks(yticks)
    # plt.set_ylabel("Speedup", fontsize=font_size, fontweight="bold")

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

    # plt.legend(
    #     fontsize=font_size - 4,
    #     edgecolor="k",
    #     ncol=1,
    #     loc="upper center",
    #     bbox_to_anchor=(0.3, 0.99),
    # )


def draw_acc(plt, data, yticks, xlabel=True):
    xtile, xdata, heads, ydata = data
    name = "Test Accuracy"

    plt.set_title(name, fontsize=font_size, y=1.02, x=0.5, fontweight="bold")
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
    if yticks[-1] > ymax:
        yticks = yticks[:-1]
    plt.set_ylim(ymin, ymax)
    plt.set_yticks(yticks)
    plt.set_ylabel("$\Delta$acc(%)", fontsize=font_size)

    cluster_num = len(xdata)
    per_cluster_bar_num = len(heads) + 1
    all_bar_num = cluster_num * per_cluster_bar_num + 1
    bar_width = (xmax - xmin) / all_bar_num
    print(bar_width)

    for it, head in enumerate(heads):
        cluster_witdh = bar_width * len(heads)
        plot_x = xticks[1:-1]
        plot_x -= cluster_witdh / 2  # start offset of bar cluster
        plot_x += bar_width * (it + 0.5)  # start offset of this bar

        plot_y = []
        plot_label = []
        for v in ydata[head]:
            plot_y.append(v)
            plot_label.append("{:.4f}".format(v))

        container = plt.bar(
            plot_x,
            plot_y,
            width=bar_width,
            edgecolor="k",
            hatch=hatch_list[it],
            color=color_list[it + 1],
            label=head,
            zorder=10,
        )

        plt.plot(
            [xmin, xmax],
            [0, 0],
            linewidth=1,
            linestyle='-',
            color='k',
            clip_on=False,
            zorder=0,
        )

        # plt.legend(
        #     fontsize=font_size - 4,
        #     edgecolor="k",
        #     ncol=2,
        #     loc="upper center",
        #     bbox_to_anchor=(0.5, 1),
        # )


if __name__ == "__main__":
    plt.figure(figsize=(9, 2.5))
    plt.subplots_adjust(wspace=0.4, hspace=0.15)
    plt.clf()

    speed_data = read_data("data/products_layers_speed.csv")
    draw_speed(plt.subplot(1, 2, 1), speed_data, (1, 4, 1.5), xlabel=True)

    acc_data = read_data("data/products_layers_acc.csv")
    draw_acc(plt.subplot(1, 2, 2), acc_data, (-1.0, 0.5, 0.5), xlabel=True)

    plt.xlabel("#GNN Layers",
               fontsize=font_size,
               labelpad=5,
               x=-0.13,
               fontweight="bold")

    save_path = "figures/layer_speed_accuracy.pdf"
    print(f"[Note]Save to {save_path}")
    plt.savefig(save_path, bbox_inches="tight")
    plt.close("all")
