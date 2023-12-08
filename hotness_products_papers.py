import numpy as np
import matplotlib.pyplot as plt
import os

def read_data(path):
    presampling_hotness = []
    presampling_cdf = []
    # read from path, it's a txt, and every line is have two numbers seperated by a comma and a space
    # like 0.004464285913854837, 0.007593785967272909
    # use regex 
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                hotness, cdf = line.split(", ")
                presampling_hotness.append(float(hotness))
                presampling_cdf.append(float(cdf))
    return presampling_hotness, presampling_cdf

def draw_figure(size):
    color_list = ["#c18076", "#819fa6"]
    font_size = 18
    plt.figure(figsize=(4,3.5))
    path = f"data/PD_{size}_hotness.txt"
    PD_presampling_hotness, PD_presampling_cdf = read_data(path)
    plt.plot(PD_presampling_hotness, PD_presampling_cdf, label="PD",  color=color_list[0])
    path = f"data/PP_{size}_hotness.txt"
    PP_presampling_hotness, PP_presampling_cdf = read_data(path)
    plt.plot(PP_presampling_hotness, PP_presampling_cdf, label="PP",  color=color_list[1])
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
    xticks = np.arange(0, 1.1, 0.2)
    yticks = np.arange(0, 1.1, 0.2)
    plt.xticks(xticks, fontsize=font_size, fontweight="light")
    plt.yticks(yticks, fontsize=font_size, fontweight="light")
    plt.xlabel("Hotness", fontsize=font_size, fontweight="light")
    plt.ylabel("CDF", fontsize=font_size, fontweight="light")
    plt.legend(
        fontsize=10,
        edgecolor="k",
        ncol=1,
        loc="lower right",
    )
    save_path = os.path.expanduser(f'figures/PD_PP_{size}_hotness_cdf.pdf')
    plt.savefig(save_path, bbox_inches="tight")
    plt.close("all")


def draw():
    draw_figure("mini_batch")
    draw_figure("whole_graph")

    plt.close("all")


if __name__ == "__main__":
    draw()