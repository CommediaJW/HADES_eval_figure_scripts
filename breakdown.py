import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

hatch_list = [None, "//", "\\\\",  "--"]
color_list = ["#819fa6", "#c18076", "#3d4a55", "#d1b5ab"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def read_data(path):
    labels = []
    all_data = {}
    with open(path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            new_row = []
            cur_key = row[0]
            labels.append(cur_key)
            for d in row[1:]:
                if isfloat(d) or d.isdigit():
                    new_row.append(float(d))
                else:
                    new_row.append(0)
            all_data[cur_key] = new_row

    return header, labels, all_data


def plot(headers, labels, data, output_path, max_ylim, ystep):
    plt.figure(figsize=(9, 5))
    plt.subplots_adjust(wspace=0.5)
    plt.clf()
    # fix parameter
    font_size = 20
    tick_space_len = 1
    bar_width = 0.24
    plt.rcParams['font.size'] = font_size

    # plt.title("Breakdown-GraphSAGE", fontsize=font_size + 1, y=-0.3)
    plt.tick_params(
        axis="both",
        which="major",
        labelsize=24,
        direction="in",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    xlim = len(headers) * tick_space_len
    xlabels = [""] + headers
    xticks = np.arange(0, xlim + tick_space_len, tick_space_len)

    plt.xlim(0, xlim)
    plt.xticks(xticks, xlabels)
    # plt.xlabel("Dataset", fontsize=font_size, fontweight="bold")
    
    for it, label in enumerate(labels):
        if it == 0:
            plt.ylabel(
                "Normalized Speedup",
                fontsize=font_size,
                fontweight="bold",
            )
        plt.ylim(0, max_ylim)
        plt.yticks(np.arange(0, max_ylim, ystep))
        #plt.ticklabel_format(style='scientific',
        #                     axis='y',
        #                     scilimits=(3, 3),
        #                     useMathText=True)

        plot_x = np.arange(1 * tick_space_len,
                           len(headers) * tick_space_len,
                           tick_space_len,
                           dtype=float)
        cluster_len = bar_width * len(labels)
        plot_x -= cluster_len / 2  # start offset of bar cluster
        plot_x += bar_width * (it + 0.5)  # start offset of this bar
        plot_y = []
        plot_label = []
        for e in data[label]:
            if e > 0.01:
                plot_y.append(e)
                plot_label.append("%.1f" % e)
        container = plt.bar(
            plot_x,
            plot_y,
            width=bar_width,
            edgecolor="k",
            hatch=hatch_list[it],
            color=color_list[it],
            label=label,
            zorder=10,
        )
        plt.bar_label(container, plot_label, fontsize=font_size - 2,
                     zorder=10)

    plt.legend(
        fontsize=font_size,
        edgecolor="k",
        ncol=2,
        loc="upper center",
        bbox_to_anchor=(0.5, 1),
    )
    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, max_ylim, ystep):
    header, labels, all_data = read_data(input_path)

    output_path = "figures/" + "breakdown.pdf"
    plot(header, labels, all_data, output_path, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/breakdown.csv", "figures", 5, 1)
