import random
from src.element import Element
from src.job import Job
from src.distributions import sample

class ZoneDemand(Element):
    def __init__(self, args, controller):
        super().__init__(controller)
        self.zone = args["zone"]
        self.probability = sample(args["probability"], vars(self))
        self.quantity = args["quantity"]
        self.duration = args["duration"]
        self.max_delivery_delta = args["max_delivery_delta"]

    def __call__(self):
        duration = sample(self.duration, locals())
        max_delivery_delta = sample(self.max_delivery_delta, locals())
        quantity = sample(self.quantity, locals())
        
        jobs = []
        for i in range(0, quantity):
            if random.random() <= self.probability:
                assignee = random.choice(self.controller.zones[self.zone]["nodes"])
                customer = random.choice(self.controller.zones[self.zone]["customers"])
                job = Job(
                    controller=self.controller,
                    assignee=assignee,
                    customer=customer,
                    duration=duration,
                    max_delivery_delta=max_delivery_delta,
                    zone=self.zone
                )
                self.event("job-created", job)
                jobs.append(job)
        return jobs