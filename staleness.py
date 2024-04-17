import argparse
import time
import os
import numpy as np
import torch as th
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import matplotlib.pyplot as plt


def main(args):
    print("Loading training data")
    hotness_list = th.load(
        os.path.join(args.save_path,
                     f"{args.graph_name}_hotness_processed.pt"))
    stayiters = th.load(
        os.path.join(args.save_path,
                     f"{args.graph_name}_stayiters_processed.pt"))

    sorted_hotness, sorted_indices = th.sort(hotness_list)
    sorted_threshold = (1 / sorted_hotness).ceil().int().clamp(max=35)
    sorted_stayiters = stayiters[sorted_indices]
    hotness_stayiters = th.zeros((20, ), dtype=th.float32)
    hotness_threshold = th.zeros((20, ), dtype=th.float32)
    hotness_count = th.zeros((20, ), dtype=th.float32)
    for i in range(20):
        start_value = i / 200
        end_value = (i + 1) / 200
        indices = th.where((sorted_hotness >= start_value)
                           & (sorted_hotness < end_value))
        hotness_count[i] = (start_value + end_value) / 2
        hotness_stayiters[i] = th.mean(
            th.Tensor.float(sorted_stayiters[indices]))
        hotness_threshold[i] = th.mean(
            th.Tensor.float(sorted_threshold[indices]))
    plt.plot(hotness_count, hotness_stayiters, label='Iters in buffer')
    plt.plot(hotness_count, hotness_threshold, label='Iters threshold')
    plt.xticks(np.arange(0, 0.11, 0.01))
    plt.ylabel('Iterations')
    plt.xlabel('Vertices Hotness')
    plt.title(f'{args.graph_name} staleness control')
    plt.legend()
    output_path = os.path.join('figures', f'{args.graph_name}_staleness.pdf')
    plt.savefig(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GCN")
    parser.add_argument("--graph_name", type=str, help="graph name")
    parser.add_argument("--save_path", type=str, default=".")
    args = parser.parse_args()

    print(args)
    main(args)
