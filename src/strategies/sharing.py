import numpy as np

class Sharing:
    def __init__(self):
        self.overhead_cost = 0.1
    
    def dispatch(self, nodes, jobs):
        for job in jobs:
            assignee = nodes[job.assignee]
            if (assignee.next_free_time + job.duration + job.logistic_time < job.max_delivery_time) or len(assignee.neighbours) == 0:
                assignee.dispatch(job)
            else:
                if assignee.neighbours == "*": assignee.neighbours = list(nodes.keys())
                next_free_times = [nodes[node].next_free_time for node in assignee.neighbours]
                logistic_times = [nodes[node].get_logistic_time(job) for node in assignee.neighbours]
                finish_times = [nft+lt+job.duration for nft, lt in zip(next_free_times, logistic_times)]

                new_assignee = nodes[assignee.neighbours[np.argmin(finish_times)]]
                
                new_assignee.dispatch(job)