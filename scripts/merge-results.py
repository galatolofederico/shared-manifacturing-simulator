import argparse
import pandas as pd
from matplotlib import pyplot as plt
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument("--base-folder", required=True)
parser.add_argument("--merge-folders", nargs="+", default=["NoSharing", "Sharing"])

args = parser.parse_args()

histories = dict()
zones = []
for folder in args.merge_folders:
    histories[folder] = dict()
    for zone_name in os.listdir(os.path.join(args.base_folder, folder)):
        zone_folder = os.path.join(os.path.join(args.base_folder, folder), zone_name)
        if os.path.isdir(zone_folder):
            histories[folder][zone_name] = pd.read_csv(os.path.join(zone_folder, "history.csv")).set_index("tick")
            if zone_name not in zones: zones.append(zone_name)

columns = histories[folder][zone_name].columns

print("Merging")
for zone in tqdm(zones):
    for colum in columns:
        dest_folder = os.path.join(args.base_folder, "merged", zone)
        os.makedirs(dest_folder, exist_ok=True)
        fig = plt.figure()
        plt.title(f"{zone}/{colum}")
        for label in args.merge_folders:
            df = histories[label][zone]
            plt.plot(df.index, df[colum], label=label)
        plt.legend()
        plt.savefig(os.path.join(dest_folder, f"{colum}.jpg"))
        plt.close(fig)
