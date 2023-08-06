# SolarNet

> Deep Learning for Solar Physics Prediction

The SolarNet library permits to use the different Pytorch models, datasets, preprocessing, and others utilities
developed during the SolarNet project. It also makes straightforward the download, loading, and finetuning of the big
pretrained SSL models. With SolarNet, anyone can access the datasets (at this time, only SDO-Benchmark is available
through the library) and finetune the powerful models. The library is compatible with Pytorch-Lightning, but the models
are also pure Pytorch Module and the training loop can be written from scratch.

Find the docs on [jdonzallaz.gitlab.io/solarnet](https://jdonzallaz.gitlab.io/solarnet/).

## Installation

Use pip to install:

```
pip install solarnet-lib
```

Python 3.6+ is required.

## Data

Two datasets are supported: SDO-Dataset and SDO-Benchmark. SDO-Dataset needs to be downloaded from the Stanford's servers.
The SDO-Benchmark dataset can be downloaded using the CLI:

```
solarnet download sdo-benchmark data/
```

## Dataset

```python
path = Path("data") / "sdo-benchmark" / "train"
dataset = SDOBenchmarkDataset(path)
```

Also available as a pytorch-lightning datamodule.

```py
path = Path("data") / "sdo-benchmark"
datamodule = SDOBenchmarkDatamodule(path)
```

## Model

```py
model = ImageClassification.from_pretrained("solarnet-ssl-bz-ft-sdo-benchmark")
```

## Finetuning

```py
trainer = pl.Trainer(
    max_epochs=10,
    gpus=0,
)
trainer.fit(model, datamodule=datamodule)
```

## Deployment

```bash
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
```

## Author

SolarNet is a deep learning research toolbox for solar physics. It was developed during a Master thesis
by [Jonathan Donzallaz](mailto:jonathan.donzallaz@hefr.ch).
