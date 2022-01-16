# shared-manufacturing-simulator

Repository for the paper [Blockchain-based Shared Additive Manufacturing]()

**An online demo is available [here](https://colab.research.google.com/drive/1w79YsUnnRT8T7E8NzpqcPan2p8F8aWKn?usp=sharing)**

## Installation

Clone this repository

```
git clone https://github.com/galatolofederico/shared-manufacturing-simulator.git
cd shared-manufacturing-simulator
```

Create a virtualenv with Python3.7 and install the requirements

```
virtualenv --python=python3.7 env
. ./env/bin/activate
pip install -r requirements.txt
```

## Usage

In the next lines you will find a short documentation of the simulator and the supplied scripts

### Simulation scenarios

The simulator uses `yaml` as scenario definition language. You can find an example scenario configuration file [here](./scenarios/test.yaml)

To generate the italian scenario run

```
python -m scripts.generate-scenario-italy
```

the generated scenario will be available in `./scenarios/italy.yaml`

### Running the simulator

To run the simulator for the two strategies using the generated italian scenario run

```
python simulator.py --seed 1 --scenario ./scenarios/italy.yaml --strategy Sharing --ticks 1000
python simulator.py --seed 1 --scenario ./scenarios/italy.yaml --strategy NoSharing --ticks 1000
```

the results will be available in `./results/italy.yaml/`

### Merging the results

To merge the results of the two strategies run

```
python -m scripts.merge-results --base-folder ./results/italy.yaml
```

the merged results will be available in `./results/merged/merged`


## Contributions and license

The code is released as Free Software under the [GNU/GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license. Copying, adapting and republishing it is not only allowed but also encouraged. 

For any further question feel free to reach me at  [federico.galatolo@ing.unipi.it](mailto:federico.galatolo@ing.unipi.it) or on Telegram  [@galatolo](https://t.me/galatolo)