import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

marker_list = ["s", "^", "o", "^"]
color_list = ["#3d4a55", "#c18076", "#819fa6", "#d1b5ab"]


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


def plot(names, data, output_path, max_ylim, ystep):
    plt.figure(figsize=(4,3.5))
    plt.clf()
    # fix parameter
    font_size = 18
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams['font.size'] = font_size
    #plt.title("RD-GraphSAGE", fontsize=font_size + 1, y=-0.3)
    plt.tick_params(
        axis="both",
        which="major",
        labelsize=20,
        direction="in",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    max_xlim = len(data[names[0]]) + 1
    plt.xlim(0, max_xlim)
    x = np.arange(1, max_xlim)
    xticks = np.arange(0, max_xlim + 1, 4)
    plt.ylim(0, max_ylim)
    yticks = np.arange(ystep, max_ylim + ystep, ystep)
    plt.xlabel("Epoch", fontsize=font_size, fontweight="light")
    plt.ylabel("Valid Accuracy", fontsize=font_size, fontweight="light")
    plt.xticks(xticks, fontsize=font_size, fontweight="light")
    plt.yticks(yticks, fontsize=font_size, fontweight="light")
    for it, name in enumerate(names):
        print(data[name])
        plt.plot(x,
                 data[name],
                 label=name,
                 linestyle='-',
                 color='k',
                 marker=marker_list[it],
                 markerfacecolor=color_list[it],
                 markersize=7,
                 markeredgecolor='k',
                 markeredgewidth=0.8)

    plt.legend(
        fontsize=10,
        edgecolor="k",
        ncol=1,
        loc="lower right",
    )
    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, max_ylim, ystep):
    header, all_data = read_data(input_path)

    output_path = "figures/" + "accuracy_products_graghsage_dgl_block0_2.pdf"
    plot(header, all_data, output_path, max_ylim, ystep)


if __name__ == "__main__":
    import matplotlib.font_manager
    fonts = matplotlib.font_manager.FontProperties().get_family()[0]
    print(fonts)
    draw_figure("data/accuracy_products_graghsage_dgl_block0_2.csv", "figures", 1, 0.2)
