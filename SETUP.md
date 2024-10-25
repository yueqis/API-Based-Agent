# Setting Up

## Start the server

### 1. Requirements
* Linux, Mac OS, or [WSL on Windows](https://learn.microsoft.com/en-us/windows/wsl/install)  [ Ubuntu <= 22.04]
* [Docker](https://docs.docker.com/engine/install/) (For those on MacOS, make sure to allow the default Docker socket to be used from advanced settings!)
* [Python](https://www.python.org/downloads/) = 3.12
* [NodeJS](https://nodejs.org/en/download/package-manager) >= 18.17.1
* [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) >= 1.8
* netcat => sudo apt-get install netcat

Make sure you have all these dependencies installed before moving on to `make build`.

#### Develop without sudo access
If you want to develop without system admin/sudo access to upgrade/install `Python` and/or `NodeJs`, you can use `conda` or `mamba` to manage the packages for you:

```bash
# Download and install Mamba (a faster version of conda)
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

# Install Python 3.12, nodejs, and poetry
mamba install python=3.12
mamba install conda-forge::nodejs
mamba install conda-forge::poetry
```

### 2. Build and Setup The Environment
Begin by building the project which includes setting up the environment and installing dependencies. This step ensures that OpenHands is ready to run on your system:

```bash
make build
```

### 3. Configuring the Language Model

We use GPT-4o as our base language model, but feel free to explore other language models!

Steps for configuration:

(1) in `config.toml`, add you `api_key`.
(2) in `config.toml`, change `base_url` to match your organization's `litellm` base url

#### Configure the LM of your choice
*If you would like to change the setting of the experiment*, do:

   ```bash
   make setup-config
   ```

   This command will prompt you to enter the LLM API key, model name, and other variables ensuring that OpenHands is tailored to your specific needs. Note that the model name will apply only when you run headless. If you use the UI, please set the model in the UI.

   Note: If you have previously run OpenHands using the docker command, you may have already set some environmental variables in your terminal. The final configurations are set from highest to lowest priority:
   Environment variables > config.toml variables > default variables

For a full list of the LM providers and models available, please consult the [litellm documentation](https://docs.litellm.ai/docs/providers).
