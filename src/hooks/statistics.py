import os
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm

class Statistics:
    def __init__(self, controller):
        self.controller = controller
        self.running_stats = dict()
        for zone in self.controller.zones:
            self.running_stats[zone] = self.get_init_running_stats()
        self.history = dict()
    
    def get_init_running_stats(self):
        return dict(
            total_jobs = 0,
            active_jobs = 0,
            finished_jobs = 0,
            failed_jobs = 0,
        )
    
    def get_init_tick_stats(self):
        return dict(
            total_backlog = 0,
            active_machines = 0,
            total_machines = 0
        )
    
    def tick(self):
        tick_stats = dict()
        for zone in self.controller.zones:
            tick_stats[zone] = self.get_init_tick_stats()

        for nid, node in self.controller.nodes.items():
            for queue in node.queues:
                for zone in node.zones:
                    if len(queue) > 1:
                        tick_stats[zone]["total_backlog"] += len(queue) - 1

                    if len(queue) > 0:
                        tick_stats[zone]["active_machines"] += 1
                    
                    tick_stats[zone]["total_machines"] += 1

        
        for zone in self.controller.zones:
            tick_stats[zone]["service_level"] = 1
            if zone in self.running_stats and self.running_stats[zone]["finished_jobs"] > 0 and self.running_stats[zone]["failed_jobs"] > 0:
                tick_stats[zone]["service_level"] = self.running_stats[zone]["finished_jobs"] / (self.running_stats[zone]["finished_jobs"] + self.running_stats[zone]["failed_jobs"])


        for zone in self.controller.zones:
            if zone not in self.history:
                self.history[zone] = []
            self.history[zone].append(dict(
                tick=self.controller.t,
                total_backlog=tick_stats[zone]["total_backlog"],
                total_jobs=self.running_stats[zone]["total_jobs"],
                active_jobs=self.running_stats[zone]["active_jobs"],
                finished_jobs=self.running_stats[zone]["finished_jobs"],
                failed_jobs=self.running_stats[zone]["failed_jobs"],
                utilization_rate=tick_stats[zone]["active_machines"]/tick_stats[zone]["total_machines"],
                service_level=tick_stats[zone]["service_level"],
                finished_jobs_perc=self.running_stats[zone]["finished_jobs"]/self.running_stats[zone]["total_jobs"] if self.running_stats[zone]["total_jobs"] > 0 else 0,
                failed_jobs_perc=self.running_stats[zone]["failed_jobs"]/self.running_stats[zone]["total_jobs"] if self.running_stats[zone]["total_jobs"] > 0 else 0,
            ))
    
    def event(self, name, *args):
        zones = []
        if name[:3] == "job":
            job = args[0]
            zones.append(job.zone)
        
        for zone in zones:
            if name == "job-finished":
                self.running_stats[zone]["active_jobs"] -= 1
                self.running_stats[zone]["finished_jobs"] += 1
            
            elif name == "job-created":
                self.running_stats[zone]["total_jobs"] += 1
                self.running_stats[zone]["active_jobs"] += 1

            elif name == "job-failed":
                self.running_stats[zone]["active_jobs"] -= 1
                self.running_stats[zone]["failed_jobs"] += 1
        
    def save(self, folder, save_plots=True):
        print("Saving")
        for zone in tqdm(self.controller.zones, total=len(self.controller.zones)):
            zone_history = pd.DataFrame(self.history[zone]).set_index("tick")
            zone_folder = os.path.join(folder, zone)

            os.makedirs(zone_folder, exist_ok=True)
            zone_history.to_csv(os.path.join(zone_folder, "history.csv"))
            
            if save_plots:
                for colum in zone_history.columns:
                    fig = plt.figure()
                    plt.title(colum)
                    plt.plot(zone_history.index, zone_history[colum])
                    plt.savefig(os.path.join(zone_folder, f"{colum}.jpg"))
                    plt.close(fig)