#!/bin/bash

WORKSPACE=$(pwd)
BENCHMARK_BACKEND=cuda
BENCHMARK_CXX_COMPILER=${HOME}/Kokkos/kokkos/bin/nvcc_wrapper
BENCHMARK_DEVICE=h100


${WORKSPACE}/lapisBuild/bin/lapis-algebraic-kernel-fusion-benchmark \
  --backend ${BENCHMARK_BACKEND} \
  --kokkos-root ${HOME}/Kokkos/kokkos/build \
  --cxx ${BENCHMARK_CXX_COMPILER} \
  --lapis-opt ${WORKSPACE}/lapisBuild/bin/lapis-opt \
  --lapis-translate ${WORKSPACE}/lapisBuild/bin/lapis-translate \
  --support-lib ${WORKSPACE}/dependencies/llvmInstall/lib/libmlir_c_runner_utils.so \
  --case all \
  --warmup 5 \
  --iterations 20 \
  --label h100 \
  --output benchmarks/algebraic_kernel_fusion/results/${BENCHMARK_DEVICE}.json
