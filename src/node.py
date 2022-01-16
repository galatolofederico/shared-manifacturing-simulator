import numpy as np
from src.element import Element
from src.distributions import sample

class Node(Element):
    def __init__(self, args, controller):
        super().__init__(controller)
        self.name = args["name"]
        self.capacity = sample(args["capacity"], self)
        self.zones = args["zones"]
        self.logistics = []
        for logistic in args["logistics"]:
            self.logistics.append(dict(
                cost=logistic["cost"],
                zone=logistic["zone"]
            ))
        self.neighbours = args["neighbours"]
        self.queues = [[] for i in range(0, self.capacity)]

    def get_logistic_time(self, job):
        for logistic in self.logistics:
            zone = self.controller.zones[logistic["zone"]]
            if self.name in zone["nodes"] and job.customer in zone["customers"]:
                cost = sample(logistic["cost"], locals())
                return cost + cost*self.overhead_cost

    @property
    def best_queue(self):
        next_free_times = [self.t + sum([job.missing_work for job in queue]) for queue in self.queues]
        return self.queues[np.argmin(next_free_times)]

    @property
    def next_free_time(self):
        next_free_times = [self.t + sum([job.missing_work for job in queue]) for queue in self.queues]
        return min(next_free_times)

    def dispatch(self, job):
        job.assignee = self.name
        self.best_queue.append(job)
    
    def __repr__(self):
        return f"<Node name={self.name}>"
    
    def tick(self):
        for i, q in enumerate(self.queues):
            if len(self.queues[i]) > 0:
                self.queues[i][0].work()
                if self.queues[i][0].finished:
                    finished_job = self.queues[i].pop(0)
                    self.event("job-finished", finished_job, self)
        
        for queue in self.queues:
            for job in queue[:]:
                if job.failed:
                    self.event("job-failed", job, self)
                    queue.remove(job)
    