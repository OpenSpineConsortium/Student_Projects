#!/usr/bin/env bash
#SBATCH --job-name=osc_make_env
#SBATCH -q primary
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
# =============================================================================
# make_env.sh — build the `osc` environment on the grid, as a job (it takes minutes and
# the login node is not for that).
#
#   cd ~/Student_Projects && mkdir -p logs && sbatch templates/make_env.sh
#
# Installs Miniforge into ~/miniforge3 if no conda is there yet, then creates (or updates)
# the environment named in templates/environment.yml. Safe to rerun.
# =============================================================================
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"

if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
  CONDA_SH="$HOME/miniforge3/etc/profile.d/conda.sh"
elif [ -f "$HOME/mambaforge/etc/profile.d/conda.sh" ]; then
  CONDA_SH="$HOME/mambaforge/etc/profile.d/conda.sh"
else
  echo "installing Miniforge into $HOME/miniforge3"
  curl -sSL -o /tmp/miniforge_$$.sh \
    "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
  bash /tmp/miniforge_$$.sh -b -p "$HOME/miniforge3"
  rm -f /tmp/miniforge_$$.sh
  CONDA_SH="$HOME/miniforge3/etc/profile.d/conda.sh"
fi
source "$CONDA_SH"

if conda env list | grep -q '^osc '; then
  echo "updating osc from templates/environment.yml"
  mamba env update -n osc -f templates/environment.yml --prune
else
  echo "creating osc from templates/environment.yml"
  mamba env create -n osc -f templates/environment.yml
fi
conda activate osc
python -c "import nibabel, numpy, scipy, matplotlib; print('osc ready:', nibabel.__version__, numpy.__version__)"
echo "done $(date)"
