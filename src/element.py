

class Element:
    def __init__(self, controller):
        self.controller = controller
    
    @property
    def t(self):
        return self.controller.t
    
    @property
    def overhead_cost(self):
        return self.controller.strategy.overhead_cost

    def event(self, event, *args):
        self.controller.event(event, *args)
        