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


def plot(names, data, output_path, max_xlim, xstep, min_ylim, max_ylim, ystep,
         ytile, speeduplow, speeduphigh, speeduparrowy, speeduptextx,
         speeduptexty, converge_threshold):
    for name in names:
        thisdata = data[name]
        data[name] = [[], []]
        for it, acc in enumerate(thisdata[1]):
            data[name][0].append(thisdata[0][it])
            data[name][1].append(thisdata[1][it])
            if acc >= converge_threshold:
                break
    print(data)

    plt.figure(figsize=(4.2, 2.5))
    plt.clf()
    # fix parameter
    font_size = 20
    plt.rcParams['font.size'] = font_size
    # plt.title("PD-GraphSAGE", fontsize=font_size + 1, y=-0.3)
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
    plt.xlim(0, max_xlim)
    # x = np.arange(1, max_xlim)
    xticks = np.arange(0, max_xlim + 1, xstep)
    plt.ylim(min_ylim, max_ylim)
    yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    plt.xlabel("Time (sec)", fontsize=font_size)
    if ytile:
        plt.ylabel("Test Accuracy", fontsize=font_size)
    plt.xticks(xticks)
    plt.yticks(yticks)
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

    plt.legend(
        fontsize=font_size - 2,
        edgecolor="k",
        ncol=1,
        loc="upper center",
        bbox_to_anchor=(0.69, 0.55),
    )

    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path,
                output_path,
                max_xlim,
                xstep,
                min_ylim,
                max_ylim,
                ystep,
                ytile,
                speeduplow,
                speeduphigh,
                speeduparrowy,
                speeduptextx,
                speeduptexty,
                converge_threshold=1):
    header, all_data = read_data(input_path)
    plot(header, all_data, output_path, max_xlim, xstep, min_ylim, max_ylim,
         ystep, ytile, speeduplow, speeduphigh, speeduparrowy, speeduptextx,
         speeduptexty, converge_threshold)


if __name__ == "__main__":
    draw_figure("data/accuracy_time_graphsage_products.csv",
                "figures/accuracy_time_graphsage_products.pdf", 250, 125, 0, 1,
                0.5, True, 0.5, 0.95, 0.78, 146, 0.58, 0.741)
    draw_figure("data/accuracy_time_graphsage_reddit.csv",
                "figures/accuracy_time_graphsage_reddit.pdf", 80, 40, 0, 1,
                0.5, True, 0.53, 0.95, 0.77, 45, 0.62, 0.93)
    draw_figure("data/accuracy_time_gat_products.csv",
                "figures/accuracy_time_gat_products.pdf", 250, 125, 0.5, 1,
                0.25, True, 0.76, 0.95, 0.83, 137, 0.85, 0.79)
    draw_figure("data/accuracy_time_gat_reddit.csv",
                "figures/accuracy_time_gat_reddit.pdf", 60, 30, 0.5, 1, 0.25,
                True, 0.77, 0.95, 0.86, 38.5, 0.79, 0.921)
