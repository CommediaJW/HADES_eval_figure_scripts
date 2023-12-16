import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

marker_list = ["o", "^", "s", "v", "*"]
color_list = ["#c18076", "#819fa6", "#3d4a55", "#d1b5ab", "#E7D3C7"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def get_labels(data):
    for key, value in data.items():
        return [label[0] for label in value]


def normalize(data):
    for name in data:
        if name != "Hot Threshold":
            for i in range(len(data[name]) - 1, -1, -1):
                data[name][i] /= data[name][0]
    return data


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
    normalize(all_data)
    print(all_data)

    return header, all_data


def plot(names, data, output_path, max_ylim, ystep):
    plt.figure(figsize=(9, 2.5))
    plt.clf()
    # fix parameter
    font_size = 20
    plt.rcParams['font.size'] = font_size
    # plt.title("PD-GraphSAGE", fontsize=font_size + 1, y=-0.35)
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
    max_xlim = len(data[names[0]])
    plt.xlim(0, max_xlim - 1)
    xticks = np.arange(0, max_xlim)
    xlabels = data[names[0]]
    plt.ylim(0, max_ylim)
    yticks = np.arange(ystep, max_ylim + ystep, ystep)
    plt.xlabel(names[0], fontsize=font_size, labelpad=10)
    plt.ylabel("Hot Nodes Ratio", fontsize=font_size, labelpad=10)
    plt.xticks(xticks, xlabels)
    plt.tick_params(axis='x', pad=15)
    plt.yticks(yticks)
    plt.tick_params(axis='y', pad=10)
    for it, name in enumerate(names):
        if it == 0:
            continue
        plt.plot(
            xticks,
            data[name],
            label=name,
            linestyle='-',
            color='k',
            marker=marker_list[it - 1],
            markerfacecolor=color_list[it - 1],
            markersize=8,
            markeredgecolor='k',
            clip_on=False,
            zorder=10 - it,
        )

    if len(names) > 2:
        plt.legend(
            fontsize=font_size,
            edgecolor="k",
            ncol=1,
            loc="upper center",
            bbox_to_anchor=(0.87, 0.98),
        )

    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, max_ylim, ystep):
    header, all_data = read_data(input_path)

    output_path = "figures/" + "threshold_hot_nodes_rate.pdf"
    plot(header, all_data, output_path, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/threshold_hot_nodes_rate.csv", "figures", 1.0, 0.5)
