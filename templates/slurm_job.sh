#!/usr/bin/env bash
#SBATCH --job-name=osc_measure
#SBATCH -q primary
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
# =============================================================================
# slurm_job.sh — run one Python script over the dataset on the WSU grid.
#
#   mkdir -p logs
#   sbatch templates/slurm_job.sh projects/<you>/measure_something.py --workers 8
#
# What each line above means: the queue is "primary"; one node, one task, eight CPUs (match
# the --workers of your script); 32 GB of memory; two hours of wall time; stdout and stderr
# go to logs/ named by job name and job id. Ask for what you need, not more: shorter and
# smaller jobs start sooner.
# =============================================================================
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"

# the mamba environment created from templates/environment.yml
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate osc

echo "job $SLURM_JOB_ID on $(hostname), $(date)"
echo "running: python $*"
python "$@"
echo "finished $(date)"
