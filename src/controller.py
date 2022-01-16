import io
import tqdm

class Controller:
    def __init__(self):
        self.t = 0
        self.strategy = None
        self.nodes = dict()
        self.demands = []
        self.hooks = []
        self.zones = None
        self.log_fd = io.StringIO()

    def set_strategy(self, strategy):
        assert self.strategy is None
        self.strategy = strategy
    
    def add_node(self, node):
        self.nodes[node.name] = node

    def add_demand(self, demand):
        self.demands.append(demand)
    
    def set_zones(self, zones):
        self.zones = zones
    
    def add_hook(self, hook):
        self.hooks.append(hook)

    def get_jobs(self):
        tick_jobs = []
        for demand in self.demands:
            tick_jobs.extend(demand())
        return tick_jobs

    def tick(self):
        self.t += 1
        tick_jobs = self.get_jobs()
        self.strategy.dispatch(self.nodes, tick_jobs)
        for nid, n in self.nodes.items():
            n.tick()
        for hook in self.hooks: 
            hook.tick()

    def event(self, name, *args):
        self.log_fd.write(f"[T={self.t}] <{name}> ({args})\n")
        for hook in self.hooks: hook.event(name, *args)
    
    def run(self, ticks):
        for t in tqdm.trange(0, ticks):
            self.tick()
        
    def save_logs(self, filename):
        with open(filename, "w") as f:
            self.log_fd.seek(0)
            f.write(self.log_fd.read())
            self.log_fd.close()