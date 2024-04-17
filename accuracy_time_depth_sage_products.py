import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

color_list = ["#c18076", "#819fa6", "#3d4a55", "#d1b5ab"]
line_list = ["-", "--", "-.", ":"]


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
        for name in header:
            all_data[name] = [[], []]
        for row in reader:
            for i in range(int(len(row) / 2)):
                all_data[header[i]][0].append(float(row[i * 2 + 0]))
                all_data[header[i]][1].append(float(row[i * 2 + 1]))

    return header, all_data


def plot(plt, title, names, data, output_path, max_xlim, xstep, min_ylim,
         max_ylim, ystep, xtile, ytile, speeduplow, speeduphigh, speeduparrowy,
         speeduptextx, speeduptexty, converge_threshold):
    for name in names:
        thisdata = data[name]
        data[name] = [[], []]
        for it, acc in enumerate(thisdata[1]):
            data[name][0].append(thisdata[0][it])
            data[name][1].append(thisdata[1][it])
            if acc >= converge_threshold:
                break
    print(data)

    # plt.figure(figsize=(4.2, 2.5))
    # plt.clf()
    # fix parameter
    font_size = 20
    # plt.rcParams['font.size'] = font_size
    # plt.title("PD-GraphSAGE", fontsize=font_size + 1, y=-0.3)
    plt.set_title(title, fontsize=font_size, y=-0.6, fontweight="bold")
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
    plt.set_xlim(0, max_xlim)
    # x = np.arange(1, max_xlim)
    xticks = np.arange(0, max_xlim + 1, xstep)
    plt.set_ylim(min_ylim, max_ylim)
    yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    ylabel = []
    for y in yticks:
        ylabel.append("{:.2f}".format(y))
    if xtile:
        plt.set_xlabel("Time (sec)", fontsize=font_size)
    if ytile:
        plt.set_ylabel("Test Accuracy", fontsize=font_size, x=-1)
    plt.set_xticks(xticks)
    plt.set_yticks(yticks, ylabel)
    end_list = []
    for it, name in enumerate(names):
        plt.plot(data[name][0],
                 data[name][1],
                 label=name,
                 linestyle=line_list[it],
                 color=color_list[it])
        end_list.append(data[name][0][-1])

    end_list.sort()
    for end in end_list:
        plt.plot([end, end], [speeduplow, speeduphigh],
                 linestyle='--',
                 color='k')
    plt.annotate('',
                 xy=(end_list[1], speeduparrowy),
                 xytext=(end_list[0], speeduparrowy),
                 arrowprops=dict(arrowstyle='<->', color='k'))
    plt.text(speeduptextx,
             speeduptexty,
             "{:.2f}x".format(end_list[1] / end_list[0]),
             fontsize=font_size - 2)
    # plt.ticklabel_format(style='scientific',
    #                      axis='y',
    #                      scilimits=(1, 1),
    #                      useMathText=True)


def draw_figure(ax,
                title,
                input_path,
                output_path,
                max_xlim,
                xstep,
                min_ylim,
                max_ylim,
                ystep,
                xtile,
                ytile,
                speeduplow,
                speeduphigh,
                speeduparrowy,
                speeduptextx,
                speeduptexty,
                converge_threshold=1):
    header, all_data = read_data(input_path)
    plot(ax, title, header, all_data, output_path, max_xlim, xstep, min_ylim,
         max_ylim, ystep, xtile, ytile, speeduplow, speeduphigh, speeduparrowy,
         speeduptextx, speeduptexty, converge_threshold)


if __name__ == "__main__":
    plt.figure(figsize=(14, 7))
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    plt.clf()
    font_size = 20
    tick_space_len = 1
    # draw_figure(plt.subplot(2, 2, 1), "PD-GraphSAGE-2layer",
    #             "data/accuracy_time_graphsage_products_2layer.csv",
    #             "figures/accuracy_time_graphsage_products_2layer.pdf", 100, 50,
    #             0, 1, 0.5, True, True, 0.5, 0.9, 0.65, 69, 0.75, 0.723)
    draw_figure(plt.subplot(2, 3, 1), "PD-GraphSAGE-3layer",
                "data/accuracy_time_graphsage_products.csv",
                "figures/accuracy_time_graphsage_products.pdf", 250, 125, 0, 1,
                0.5, True, True, 0.5, 0.95, 0.78, 146, 0.58, 0.741)
    draw_figure(plt.subplot(2, 3, 2), "PD-GraphSAGE-4layer",
                "data/accuracy_time_graphsage_products_4layer.csv",
                "figures/accuracy_time_graphsage_products_4layer.pdf", 350,
                175, 0, 1, 0.5, True, False, 0.5, 0.95, 0.85, 173, 0.7, 0.7)
    draw_figure(plt.subplot(2, 3, 3), "PD-GraphSAGE-6layer",
                "data/accuracy_time_graphsage_products_6layer.csv",
                "figures/accuracy_time_graphsage_products_6layer.pdf", 1700,
                850, 0, 0.6, 0.3, True, False, 0.3, 0.58, 0.45, 900, 0.47, 1)
    draw_figure(plt.subplot(2, 3, 4), "PD-GAT-3layer",
                "data/accuracy_time_gat_products.csv",
                "figures/accuracy_time_gat_products.pdf", 250, 125, 0.5, 1,
                0.25, True, True, 0.76, 0.95, 0.83, 137, 0.85, 0.79)
    draw_figure(plt.subplot(2, 3, 5), "PD-GAT-4layer",
                "data/accuracy_time_gat_products_4layer.csv",
                "figures/accuracy_time_gat_products_4layer.pdf", 280, 140, 0,
                1, 0.5, True, False, 0.5, 0.95, 0.8, 147, 0.6, 0.78)
    plt.legend(
        fontsize=font_size - 2,
        edgecolor="k",
        ncol=2,
        loc="upper center",
        bbox_to_anchor=(0.5, 3.2),
    )
    print(f"[Note]Save to figures/accuracy_time_depth_products.pdf")
    plt.savefig("figures/accuracy_time_depth_products.pdf",
                bbox_inches="tight")
    plt.close("all")
