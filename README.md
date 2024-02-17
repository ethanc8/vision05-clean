# vision05

## Usage

After installing the dependencies, run:

```bash
conda activate vision05
python3 targetviewer/main.py
```

You can take headshots by clicking on a person ("Target") and using the "Take headshots" tool. Press <kbd>SPACE</kbd> to take a picture, and press <kbd>Esc</kbd> to exit the "Take headshots" tool. Next, go to "Administrative Settings", use the "Pickle embeddings" tool to pickle the embeddings, and then use the "Begin face recognition" tool to begin face recognition. It will take up the entire screen. Press <kbd>Esc</kbd> to exit the face recognition program and return to the main screen.

## Dependencies installation

### Install conda/miniforge

First, please have Conda installed on your computer. If it's not installed, please install [Miniforge3](https://conda-forge.org/miniforge/), which includes Conda and a conda-forge based Python environment. You can install Miniforge3 using the following command:

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
rm Miniforge3-$(uname)-$(uname -m).sh
```

Close and reopen your shell, and run:

```bash
# Prevent Conda from polluting your environment when you're not working on Conda-managed projects.
conda config --set auto_activate_base false
```

## Install dependencies (x86_64)

Now, you can use Conda to install the dependencies.

```bash
conda env create -f environment.yml
conda activate vision05
```

If you modify `environment.yml`, please run

```bash
conda env update -f environment.yml
```

## Install dependencies (Raspberry Pi)

Now, you can use Conda to install the dependencies.

```bash
sudo apt install yad
conda env create -f environment-rpi.yml
conda activate vision05
```

If you modify `environment.yml`, please run

```bash
conda env update -f environment-rpi.yml
```