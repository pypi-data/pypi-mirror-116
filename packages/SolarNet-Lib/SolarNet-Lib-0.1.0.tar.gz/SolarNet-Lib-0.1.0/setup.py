from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="SolarNet-Lib",
    version="0.1.0",
    description="Deep Learning for Solar Physics Prediction",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jdonzallaz/solarnet",
    author="Jonathan Donzallaz",
    author_email="jonathan.donzallaz@hefr.ch",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["solarnet=solarnet.main:app"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "boto3>=1.17.49",
        "colorlog>=5.0.0",
        "click>=7.1.1, <7.2.0",
        "lightning-bolts>=0.3.4",
        "matplotlib>=3.3.4",
        "numpy>=1.17.2",
        "pandas>=1.1.5",
        "Pillow>=8.2.0",
        "pyarrow>=4.0.0",
        "pytorch-lightning>=1.3.8",
        "ruamel.yaml>=0.16.1",
        "sunpy[net]>=2.0.0, <3.0.0",
        "torch>=1.6",
        "torchmetrics>=0.4.1",
        "torchvision>=0.7",
        "tqdm>=4.41.0",
        "typer>=0.3.2",
    ],
    zip_safe=False,
)
