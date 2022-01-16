import uuid

from src.element import Element

class Job(Element):
    def __init__(self, controller, assignee, customer, duration, max_delivery_delta, zone):
        super().__init__(controller)
        self.id = str(uuid.uuid4())
        self.assignee = assignee
        self.customer = customer
        self.duration = duration
        self.max_delivery_time = controller.t + max_delivery_delta
        self.zone = zone

        self.creation_tick = controller.t
        self.work_done = 0
        self.missing_work = self.duration
        self.logistic_time_cache = dict()

    @property
    def finished(self):
        return self.work_done >= self.duration

    @property
    def end_time(self):
        return self.t + self.missing_work

    @property
    def logistic_time(self):
        return self.controller.nodes[self.assignee].get_logistic_time(self)

    @property
    def failed(self):
        return self.end_time + self.logistic_time >= self.max_delivery_time

    def work(self):
        self.work_done += 1
        self.missing_work -= 1
        assert self.missing_work >= 0
        assert self.work_done <= self.duration
    
    def __repr__(self):
        return f"<Job id={self.id} assignee={self.assignee} customer={self.customer} creation_tick={self.creation_tick} duration={self.duration:d} max_delivery_time={self.max_delivery_time:.2f} work_done={self.work_done:d}>"