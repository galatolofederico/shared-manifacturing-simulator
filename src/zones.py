from src.element import Element

class Zones(Element):
    def __init__(self, args, controller):
        super().__init__(controller)
        self.zones = dict()
        for zone in args:
            self.zones[zone["name"]] = dict(
                nodes = zone["nodes"],
                customers = zone["customers"]
            )

    def __iter__(self):
        for zone in self.zones.keys():
            yield zone

    def __len__(self):
        return len(self.zones)
    
    def __getitem__(self, idx):
        return self.zones[idx]