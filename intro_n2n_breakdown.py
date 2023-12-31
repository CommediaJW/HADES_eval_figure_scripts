import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

hatch_list = ["\\\\", "//", "xx", "||", None]
color_list = ["#819fa6", "#3d4a55", "#c18076", "#d1b5ab", "#E7D3C7"]


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
    plt.figure(figsize=(9, 2.5))
    plt.subplots_adjust(wspace=0.5)
    plt.clf()
    # fix parameter
    font_size = 20
    tick_space_len = 1
    bar_width = 0.4
    plt.rcParams['font.size'] = font_size

    sum = [0, 0]
    for name in data:
        for i in range(len(data[name])):
            sum[i] += data[name][i]
    print(sum)

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
    xlim = len(headers) * tick_space_len
    xlabels = [""] + headers + [""]
    xticks = [0, 0.867, 2.133, 3]

    plt.ylim(0, xlim)
    plt.yticks(xticks, xlabels)

    for it, label in enumerate(labels):
        if it == 0:
            plt.xlabel(
                "Epoch Time (sec)",
                fontsize=font_size,
            )
        plt.xlim(0, max_ylim)
        plt.xticks(np.arange(0, max_ylim, ystep))

        plot_x = np.array([0.88, 2.12])
        plot_y = []
        plot_label = []
        for i, e in enumerate(data[label]):
            if e > 0.01:
                plot_y.append(e)
                plot_label.append("{:d}%".format(int(e / sum[i] * 100)))
        if it > 0:
            container = plt.barh(
                plot_x,
                plot_y,
                left=plot_y_,
                height=bar_width,
                edgecolor="k",
                hatch=hatch_list[it],
                color=color_list[it],
                label=label,
                zorder=10,
            )
            plot_y_ = np.add(plot_y_, plot_y)
        else:
            container = plt.barh(
                plot_x,
                plot_y,
                height=bar_width,
                edgecolor="k",
                hatch=hatch_list[it],
                color=color_list[it],
                label=label,
                zorder=10,
            )
            plot_y_ = plot_y
        if label == "Loading" or label == "Embedding Gradients Aggregation & Embedding Updating":
            fontcolor = "w" if label == "Loading" else "k"
            plt.bar_label(container,
                          plot_label,
                          fontsize=font_size - 7,
                          zorder=10,
                          color=fontcolor,
                          label_type="center")

    handles, _ = plt.gca().get_legend_handles_labels()
    reorder_handles = [
        handles[0], handles[2], handles[4], handles[1], handles[3]
    ]
    reorder_labels = [labels[0], labels[2], labels[4], labels[1], labels[3]]
    plt.legend(reorder_handles,
               reorder_labels,
               fontsize=font_size - 6,
               edgecolor="k",
               ncol=2,
               loc="upper left",
               bbox_to_anchor=(0, 1.08, 1, 0.5),
               mode="expand")
    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, max_ylim, ystep):
    header, labels, all_data = read_data(input_path)

    plot(header, labels, all_data, output_path, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/intro_n2n_breakdown.csv",
                "figures/intro_n2n_breakdown.pdf", 90, 20)
