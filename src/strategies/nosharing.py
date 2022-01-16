class NoSharing:
    def __init__(self):
        self.overhead_cost = 0
    
    def dispatch(self, nodes, jobs):
        for job in jobs:
            assignee = nodes[job.assignee]
            assignee.dispatch(job)