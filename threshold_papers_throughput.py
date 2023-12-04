import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

marker_list = ["o", "^", "o", "^"]
color_list = ["#819fa6", "#c18076", "#3d4a55", "#d1b5ab"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def get_labels(data):
    for key, value in data.items():
        return [label[0] for label in value]


def read_data(path):
    all_data = {}
    with open(path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        print(header)
        for name in header:
            all_data[name] = []
        for row in reader:
            for i in range(len(row)):
                all_data[header[i]].append(float(row[i]))
    print(all_data)

    return header, all_data


def plot(names, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(9, 5))
    plt.clf()
    # fix parameter
    font_size = 20
    plt.rcParams['font.size'] = font_size
    # plt.title("PP-GraphSAGE", fontsize=font_size + 1, y=-0.35)
    plt.tick_params(
        axis="both",
        which="major",
        labelsize=12,
        direction="in",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    max_xlim = len(data[names[0]])
    plt.xlim(0, max_xlim - 1)
    xticks = np.arange(0, max_xlim)
    xlabels = data[names[0]]
    plt.ylim(min_ylim, max_ylim)
    yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    plt.xlabel(names[0], fontsize=font_size, labelpad=10)
    plt.ylabel(names[1], fontsize=font_size, labelpad=10)
    plt.xticks(xticks, xlabels)
    plt.tick_params(axis='x', pad=15)
    plt.yticks(yticks)
    plt.tick_params(axis='y', pad=10)
    plt.ticklabel_format(style='scientific',
                         axis='y',
                         scilimits=(3, 3),
                         useMathText=True)
    for it, name in enumerate(names):
        if it == 0:
            continue
        plt.plot(
            xticks,
            data[name],
            label=name,
            linestyle='-',
            linewidth=2,
            color='k',
            marker=marker_list[it - 1],
            markerfacecolor=color_list[it - 1],
            markersize=12,
            markeredgecolor='k',
            markeredgewidth=1.5,
            clip_on=False,
            zorder=10,
        )

    if len(names) > 2:
        plt.legend(
            fontsize=font_size,
            edgecolor="k",
            ncol=1,
            loc="upper center",
            bbox_to_anchor=(0.17, 0.98),
        )

    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, min_ylim, max_ylim, ystep):
    header, all_data = read_data(input_path)

    output_path = "figures/" + "threshold_papers_throughput.pdf"
    plot(header, all_data, output_path, min_ylim, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/threshold_papers_throughput.csv", "figures", 28000,
                44000, 2000)
