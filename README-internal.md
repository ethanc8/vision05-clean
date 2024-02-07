# vision05

## Dependencies installation (on your own computer)

First, please have Conda installed on your computer. If it's not installed, please install [Miniforge3](https://conda-forge.org/miniforge/), which includes Conda and a conda-forge based Python environment.

```bash
conda env create -f environment.yml
conda activate vision05
```

If you modify `environment.yml`, please run

```bash
conda env update -f environment.yml
```