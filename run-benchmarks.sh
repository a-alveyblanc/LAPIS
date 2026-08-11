#!/bin/bash

WORKSPACE=$(pwd)
BENCHMARK_BACKEND=cuda
BENCHMARK_LABEL=h100

# OMP_PROC_BIND=spread
# OMP_PLACES=threads

${WORKSPACE}/lapisBuild/bin/lapis-algebraic-kernel-fusion-benchmark \
  --backend ${BENCHMARK_BACKEND} \
  --kokkos-root ${HOME}/Kokkos/kokkos/build \
  --cxx ${HOME}/Kokkos/kokkos/bin/nvcc_wrapper \
  --support-lib ${WORKSPACE}/dependencies/llvmInstall/lib/libmlir_c_runner_utils.so \
  --lapis-opt ${WORKSPACE}/lapisBuild/bin/lapis-opt \
  --lapis-translate ${WORKSPACE}/lapisBuild/bin/lapis-translate \
  --case all \
  --warmup 3 \
  --iterations 20 \
  --build-dir ${WORKSPACE}/benchmarks/algebraic-kernel-fusion/build-cuda \
  --label ${BENCHMARK_LABEL} \
  --output bench-results/${BENCHMARK_LABEL}.csv
