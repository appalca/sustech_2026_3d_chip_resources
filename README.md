# sustech_2026_3d_chip_resources
This repository contains the scripts and data required to reproduce the results of the use cases of the "Life Cycle Assessment of 3D Stacked Multi-Chip Assemblies: Comparison of Three Multi-Layer CMOS Image Sensors" paper published at IEEE SusTech 2026.

## Licensing
Please refer to the LICENCE.md document for the licencing rights granted for the content of this repository.

**Warning:** for some datasets in `data/appabuild_data`, other licences could apply: they are indicated in the header of the files, please read it carefully.  

### 3D integration processes data
This notably stands for the 3D integration processes impact data provided by the CEA-Leti, with works done in the IRT NANOELEC Displed program:

```
Holo, Antonin, et al. "45‐4: MicroLED Display Life Cycle Assessment." SID Symposium Digest of Technical Papers. Vol. 54. No. 1. 2023.
```

This data has been provided in this repository for information purposes. The authors would like to remind that this data is R&D data which is not certified in any way.

## Citation
For any use of the data, scripts or results in this repo, please cite:

APA style:
```
Péralta, M., & Billaud, M. (2026). Life Cycle Assessment of a 3D stacked multi-chip assemblies: comparison of three multi-layer CMOS Image Sensors. In 2026 IEEE Conference on Technologies for Sustainability (SusTech). IEEE.
```

BibTeX:
```
@inproceedings{peralta2026life,
  title={{Life} {Cycle} {Assessment} of a {3D} stacked multi-chip assemblies: comparison of three multi-layer {CMOS} {Image} {Sensors}},
  author={Péralta, Maxime and Billaud, Mathilde},
  booktitle={2026 IEEE Conference on Technologies for Sustainability (SusTech)},
  year={2026},
  organization={IEEE}
}
```

## How-to
This repo contains all the scripts and data to reproduce the results of the paper, providing you have a valid EcoInvent licence. The impact model could not be shared in this repo as it contains calculated data from EcoInvent with licensing rights. Therefore, you must first build the impact model using Appa Build.

### Install
```
git clone https://github.com/appalca/sustech_2026_3d_chip_resources.git
cd sustech_2026_3d_chip_resources
pip install -r requirements.txt
```

### Build the impact model
In order to build the impact model, you will need to use Appa Build. Please follow the installation instructions here: https://appalca.github.io/basics/getting_started.html.

To familiarize yourself with Appa Build, it is recommended to take a look at the doc: https://appalca.github.io/basics/appa_build_basics.html.

To build the impact model, make sure you exported first the environmental variables `BW_USER` and `BW_PASS` with your EcoInvent credentials. Then, run, while being at the root this repository:

`appabuild lca build data/conf/appalca.yaml data/conf/run_CIS.yaml`

Then set the build impact model (`multi_layer_CIS.yaml`) in the `data/` folder.

#### Carbon-only impact model
A carbon-only version of this impact model, using only public data sources, is currently under construction, and will be shared in this repository when available for those who don't have an EcoInvent license.

### Run the scripts
You can then run any of the python script placed in the root of this repository to produce the corresponding figure.
