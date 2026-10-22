#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset PYTHONOPTIMIZE
# Includes field, independent, product and optional external Kitamura checks (R10).
exec "${1:-python3}" -m coupled_ame
