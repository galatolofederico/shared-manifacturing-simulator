import numpy as np

def sample(dist, context=dict()):
    if isinstance(dist, list):
        assert len(dist) == 1
        dist = dist[0]

    ret = None
    if dist["type"] == "constant":
        ret = dist["value"]
    elif dist["type"] == "normal":
        ret = dist["std"] * np.random.randn() + dist["mu"]
    elif dist["type"] == "formula":
        ret = eval(dist["value"].format(**context))
    else:
        raise Exception(f"Unknown distribution: {dist['type']}")
    
    if "cast" in dist:
        if dist["cast"] == "positive_integer":
            ret = int(np.round(ret))
            if ret <= 0: ret = 1
        elif dist["cast"] == "l1norm":
            ret = np.abs(ret)
        else:
            raise Exception(f"Unknown cast {dist['cast']}")
    return ret
            