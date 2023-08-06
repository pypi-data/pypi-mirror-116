# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crainets',
 'crainets.base',
 'crainets.config',
 'crainets.essentials',
 'crainets.losses',
 'crainets.models',
 'crainets.models.ResXUNet',
 'crainets.models.UNet',
 'crainets.models.blocks',
 'crainets.models.blocks.BiFPN',
 'crainets.models.blocks.utils',
 'crainets.models.efficientnet',
 'crainets.trainer']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=5.0.1,<6.0.0',
 'flake8>=3.9.2,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'py3nvml>=0.2.6,<0.3.0',
 'pytest>=6.2.4,<7.0.0',
 'torch>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'crainets',
    'version': '0.1.1b0',
    'description': 'deep learning utility library',
    'long_description': '# CRAI-Nets <img align="right" width="150" alt="20200907_104224" src="https://user-images.githubusercontent.com/29639563/125202990-9fcd9200-e276-11eb-8e00-bde211ebe0c1.png">\n\n[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)\n[![Generic badge](https://img.shields.io/badge/contributions-welcome-<COLOR>.svg)](https://shields.io/)\n[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)\n[![License](https://img.shields.io/badge/license-BSD%204--Clause-red.svg)](https://shields.io/)\n\n#### The CRAI-Nets Project\nThis is just another model-zoo and utility library combined for developing deep learning models. The main reasons for this project to exist is to avoid boilerplate code across projects, letting others tap in on your work, making benchmarking/expermenting easy and fast while also sticking to readibility and reproducibility. The goal of the project is to include as many useful models as possible and also smart customized metrics and loss functions. The project, as of now, is aimed towards computer vision, although contribution within NLP or RL is more than welcome.\n\n\n#### Getting started\n\n##### 0. Requirements\nThe library is platform agnostic although we strongly suggest to use Linux or Mac for ML development. We also suggest to use `poetry` or `pyenv` for dependency management unless you are on Win where Conda is the defacto(satans speed to you). Make sure to have python version 3.8 or later installed.\n\n\n##### 1. Install the package\nAs recommended, use poetry to install the package by running:\n\n```\n$ poetry add crainets\n```\n\n##### 2. What you need to consider\n\nThe Trainer class you can use for simple benchmarking or fast expermenting expects mainly the following:\n\n1. A model configuration dict containing hyperparameters \n2. A dict containing your loss functions\n3. A dict containing your metrics (you can specify multiple)\n4. Train and test data that you should prep in dataloader class that inherits from the pytorch `dataset` class\n5. The model architecture imported from crainets model-zoo\n\nWe suggest to write your code modular such that configurations come from a `config.py` script and the dataloader comes from a `dataloader.py` script.\n\n##### 3. Example\n\n1. Lets write up two dataloaders that will lazy evaluate our data durng runtime when its batched for training. Cifar10 is used in this example and the only reason why is for brevity.\n\n```python\n\nimport torch\nimport torchvision\nimport testing.config as config\nimport torch.utils.data as data_utils\n\ntransform = torchvision.transforms.Compose(\n    [torchvision.transforms.ToTensor(),\n     torchvision.transforms.RandomHorizontalFlip(),\n     torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])\n\ntransform_test = torchvision.transforms.Compose(\n    [torchvision.transforms.ToTensor(),\n     torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])\n\n\ntrain = torchvision.datasets.CIFAR10(\n                    config.DATA_PATH, train=True, download=True,\n                    transform=transform)\n\n\ntest = torchvision.datasets.CIFAR10(\n                    config.DATA_PATH, train=False, download=True,\n                    transform=transform_test)\n\ntrain_loader = torch.utils.data.DataLoader(\n                        train,\n                        batch_size=config.batch_size_train,\n                        shuffle=True\n                    )\ntest_loader = torch.utils.data.DataLoader(\n                        test,\n                        batch_size=config.batch_size_test,\n                        shuffle=True\n                    )\n```\n\n\n2. Now that we have our data, lets write up a config dict for our network to use.\n\n```python\nimport os\nimport torch\n\nROOT = os.getcwd()\nDATA_PATH = os.path.join(\'/data\')\nCHCKPT = os.path.join(\'/checkpoints\')\nbatch_size_train = 100\nbatch_size_test = 50\n\nTRAIN_CONFIG = {\n        "n_gpu": 1,\n        "optimizer": {\n                "type": "Adam",\n                "args": {\n                    "lr": 1e-3,\n                    "weight_decay": 0,\n                    "amsgrad": True\n                }\n            },\n            "loss": "nll_loss",\n            "metrics": [\n                "accuracy", "top_k_acc"\n            ],\n            "lr_scheduler": {\n                "type": "StepLR",\n                "args": {\n                    "step_size": 500,\n                    "gamma": 0.1\n                }\n            },\n            "trainer": {\n                "epochs": 2,\n                "iterative": False,\n                "iterations": 5,\n                "images_pr_iteration": 100,\n                "val_images_pr_iteration": 10,\n                "save_dir": CHCKPT,\n                "save_period": 5,\n                "early_stop": 1\n                }\n            }\n\nMETRICS = {\n        \'CrossEntropy\': torch.nn.CrossEntropyLoss()\n            }\n```\n\nNote that we also included METRICS as a config in the script. We could define many more metrics in the dict than what is written in the example.\n\n3. Now lets tie it all together in a controller script for running the network. We are going to use the sexy `efficient-net` in this example.\n\n```python \n# Internal imports\nfrom data_loader import train_loader, test_loader\nfrom config import config\n\n# CRAI-Nets imports\nfrom crainets.trainer.trainer import Trainer\nfrom crainets.models.efficientnet import EfficientNet\nfrom crainets.essentials.multi_loss import MultiLoss\nfrom crainets.essentials.multi_metric import MultiMetric\n\n# specifiy the needed config\nmodel = EfficientNet.from_name(in_channels=3, num_classes=10, model_name=\'efficientnet-b0\')\nloss = [(1, torch.nn.CrossEntropyLoss())]\nloss = MultiLoss(losses=loss)\n    \n# Add metrics in the metrics dict from the config file\nmetrics = MultiMetric(config.METRICS)\n\n# Instantiate zhe class\ntrainer = Trainer(\n    model=model,\n    loss_function=loss,\n    metric_ftns=metrics,\n    config=config.TRAIN_CONFIG,\n    data_loader=train_loader,\n    valid_data_loader=test_loader,\n    seed=666,\n    accumulative_metrics=True\n)\n\n# Gut gut! Now run the network training und zmile!\ntrainer.train()\n```\n\n###### The project is mainly developed and maintained by CRAI at the university hospital of Oslo\n',
    'author': 'JonNesvold',
    'author_email': 'jon.nesvold@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
