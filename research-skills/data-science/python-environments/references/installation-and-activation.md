# Miniconda Installation & First-Time Setup

## Fresh install

```bash
cd /tmp
curl -sLO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
rm Miniconda3-latest-Linux-x86_64.sh
```

The `-b` flag runs silently (no interactive prompts). `-p` sets install path.

## Post-install: ToS acceptance (Required)

Since ~2025, Anaconda repos require Terms of Service acceptance:

```bash
export PATH="$HOME/miniconda3/bin:$PATH"
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

Without this step, `conda create` and `conda install` fail with `CondaToSNonInteractiveError`.

## Configuration

```bash
conda config --set auto_activate false
# Prevents base from auto-activating on every new shell.
# auto_activate_base is an alias; conda will suggest auto_activate.
```

## Creating the default `agent` environment

```bash
conda create -n agent python=3.12 -y
```

## Activation caveat

In the tool's terminal (non-interactive bash), `.bashrc` conda init block is NOT sourced automatically. Always use:

```bash
eval "$(/home/ubuntu/miniconda3/bin/conda shell.bash hook)"
conda activate agent
```

`conda shell.bash hook` generates the shell functions needed for `conda activate` without requiring `.bashrc` sourcing. This is the **only reliable pattern** in non-interactive shells.

## Environment location

- Base: `~/miniconda3`
- agent: `~/miniconda3/envs/agent`
- Default Python: 3.12.13
- Executables: `~/miniconda3/envs/agent/bin/python`, `~/miniconda3/envs/agent/bin/pip`
