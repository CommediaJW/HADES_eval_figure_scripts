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

def draw():
    color_list = ["#3d4a55", "#c18076", "#819fa6", "#d1b5ab"]
    line_list = ["-", "--", "-.", ":"]
    font_size = 18
    plt.figure(figsize=(5,3))
    xticks = np.arange(0, 1.1, 0.2)
    yticks = np.arange(0, 1.1, 0.2)
    plt.xticks(xticks, fontsize=font_size, fontweight="light")
    plt.yticks(yticks, fontsize=font_size, fontweight="light")
    plt.xlabel("Hotness", fontsize=font_size, fontweight="light")
    plt.ylabel("Node Ratio", fontsize=font_size, fontweight="light")

    for i in range(1, 5):
        path = f"data/PD_locality_hotness_am_{5 - i}.txt"
        presampling_hotness, presampling_cdf = read_data(path)
        plt.plot(presampling_hotness, presampling_cdf, label=f'across {5 - i} machine(s)', color=color_list[4 - i], linestyle=line_list[4 - i])
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
    plt.legend(
        fontsize=10,
        edgecolor="k",
        ncol=1,
        loc="lower right",
    )
    save_path = os.path.expanduser(f'figures/PD_locality_hotness_cdf.pdf')
    plt.savefig(save_path, bbox_inches="tight")
    plt.close("all")



if __name__ == "__main__":
    draw()