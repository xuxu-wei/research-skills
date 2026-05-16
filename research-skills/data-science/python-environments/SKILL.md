---
name: python-environments
description: "Python environment management with Miniconda: install, activate, create/destroy environments. Default env is agent (Python 3.12). Trigger on any Python task — experiments, scripts, Jupyter, tools, package installs, dependency resolution."
---

# Python Environments (Miniconda)

## Overview

All Python work uses Miniconda. The **base environment is for management only** (conda install, conda create, conda activate). Never execute tasks in base.

The **default working environment is `agent`** (Python 3.12 at `~/miniconda3/envs/agent`). Use it for all Python work unless a compatibility issue forces a new temporary env.

## Activation

Non-interactive shells (common in agent context) need explicit conda initialization:

```bash
eval "$(/home/ubuntu/miniconda3/bin/conda shell.bash hook)"
conda activate agent
```

After this, `python`, `pip`, `conda install`, etc. all run inside the `agent` env.

## Workflow

### 1. Default path — use `agent`

```bash
eval "$(/home/ubuntu/miniconda3/bin/conda shell.bash hook)"
conda activate agent
# ... run code, install packages, launch Jupyter ...
```

### 2. Package installation

Prefer `conda install <pkg>` first. Fall back to `pip install <pkg>` inside the active conda env when conda doesn't have the package. Both go into the `agent` env.

### 3. Temporary environment (only when needed)

If a package or task has unresolvable compat issues in `agent`, create a named temp env:

```bash
conda create -n <task-name> python=<ver> -y
conda activate <task-name>
# work, then delete when done
conda deactivate
conda env remove -n <task-name> -y
```

## Pitfalls

- **Do NOT use `conda activate` without prior `eval` in non-interactive shells.** The conda shell function is not defined. Always use the eval pattern above.
- **conda ToS**: As of 2025, Anaconda repos require ToS acceptance before package download. Accept once after install: `conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main` (and main/r as needed).
- **auto_activate**: Set `auto_activate false` via `conda config --set auto_activate false` so base doesn't activate on shell start.
- **Do NOT install packages into base**. Base is management-only.
- **Do NOT create a new env for every task.** Only when compatibility forces it.

## Verification

```bash
conda activate agent
python --version    # expect 3.12.x
which python        # expect ~/miniconda3/envs/agent/bin/python
which pip           # expect ~/miniconda3/envs/agent/bin/pip
```
