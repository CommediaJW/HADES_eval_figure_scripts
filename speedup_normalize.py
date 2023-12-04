import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

hatch_list = ["//", "\\\\", None, None]
color_list = ["#819fa6", "#c18076", "#3d4a55", "#d1b5ab"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def get_labels(data):
    for key, value in data.items():
        return [label[0] for label in value]


def read_data(path):
    elements = []
    labels = []
    cur_key = None
    all_data = {}
    dataeset_name = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if len(row) == 1:
                "Dataset"
                cur_key = row[0]
                all_data[cur_key] = []
                elements.clear()
                labels.clear()
                dataeset_name.append(cur_key)
            else:
                new_row = []
                for d in row[1:]:
                    if isfloat(d) or d.isdigit():
                        new_row.append(float(d))
                    else:
                        new_row.append(0)
                all_data[cur_key].append([row[0], new_row])

    labels = get_labels(all_data)

    return dataeset_name, header, labels, all_data


def plot(names, object_labels, group_labels, data, lengend, output_path,
         max_ylim, ystep, model_name):
    plt.figure(figsize=(20, 3))
    plt.subplots_adjust(wspace=0.5)
    plt.clf()
    # fix parameter
    font_size = 20
    tick_space_len = 1
    plt.rcParams['font.size'] = font_size

    for it, name in enumerate(names):
        if name == "RD" or name == "PD":
            ax = plt.subplot(1, 6, (it * 2 + 1, it * 2 + 2))
        else:
            ax = plt.subplot(1, 6, 3 + it)

        plt.title(name + "-" + model_name, fontsize=font_size, y=-0.5)
        ax.tick_params(
            axis="both",
            which="major",
            labelsize=font_size,
            direction="in",
            bottom=True,
            top=True,
            left=True,
            right=True,
        )

        if name == "RD" or name == "PD":
            xlim = 4 * tick_space_len
            xlabels = [""] + group_labels
            bar_width = 0.35
        else:
            xlim = 2 * tick_space_len
            xlabels = [""] + [group_labels[-1]]
            bar_width = 0.462
        xticks = np.arange(0, xlim, tick_space_len)
        ax.set_xlim(0, xlim)
        ax.set_xticks(xticks, xlabels)
        ax.set_xlabel("#GPUs", fontsize=font_size)

        if it == 0:
            ax.set_ylabel(
                "Speedup",
                fontsize=font_size,
            )
        ax.set_ylim(0, max_ylim)
        ax.set_yticks(np.arange(0, max_ylim, ystep))
        # ax.ticklabel_format(style='scientific',
        #                    axis='y',
        #                    scilimits=(3, 3),
        #                    useMathText=True)

        for i in range(len(object_labels)):
            if name == "RD" or name == "PD":
                plot_x = np.arange(1 * tick_space_len,
                                   4 * tick_space_len,
                                   tick_space_len,
                                   dtype=float)
            else:
                plot_x = np.array([1 * tick_space_len], dtype=float)
            cluster_len = bar_width * len(group_labels)
            plot_x -= cluster_len / 2  # start offset of bar cluster
            plot_x += bar_width * (i + 1)  # start offset of this bar
            plot_y = []
            plot_label = []
            for e in data[name][i][1]:
                if e > 0.01:
                    plot_y.append(e)
                    plot_label.append("%.1f" % e)
            print(plot_x)
            container = ax.bar(
                plot_x,
                plot_y,
                width=bar_width,
                edgecolor="k",
                hatch=hatch_list[i],
                color=color_list[i],
                label=object_labels[i],
                zorder=10,
            )
            ax.bar_label(container,
                         plot_label,
                         fontsize=font_size - 2,
                         zorder=10)

        if name == "RD" or name == "PD":
            ax.legend(
                fontsize=font_size,
                edgecolor="k",
                ncol=1,
                loc="upper center",
                bbox_to_anchor=(0.22, 1),
            )
        else:
            ax.legend(
                fontsize=font_size,
                edgecolor="k",
                ncol=1,
                loc="upper center",
                bbox_to_anchor=(0.5, 1),
            )
    plt.rcParams['font.size'] = font_size
    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, max_ylim, ystep):
    names, header, labels, all_data = read_data(input_path)

    output_path = "figures/" + "speedup_graphsage_normalize.pdf"
    plot(names, labels, header, all_data, None, output_path, max_ylim, ystep,
         "GraphSAGE")


def draw_figure2(input_path, output_path, max_ylim, ystep):
    names, header, labels, all_data = read_data(input_path)

    output_path = "figures/" + "speedup_gat_normalize.pdf"
    plot(names, labels, header, all_data, None, output_path, max_ylim, ystep,
         "GAT")


if __name__ == "__main__":
    draw_figure("data/speedup_graphsage_normalize.csv", "figures", 12, 2.5)
    draw_figure2("data/speedup_gat_normalize.csv", "figures", 12, 2.5)
