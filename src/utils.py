def seed_everything(seed):
    import random, os
    import numpy as np
    
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)