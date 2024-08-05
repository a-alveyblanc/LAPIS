//===- KokkosMemorySpaceAssignment.cpp - Pattern for kokkos-assign-memory-spaces pass --------------------===//
//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#include "CodegenUtils.h"

#include "mlir/Dialect/MemRef/IR/MemRef.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/Dialect/Kokkos/IR/KokkosDialect.h"
#include "mlir/Dialect/Kokkos/Transforms/Passes.h"
#include "mlir/IR/IRMapping.h"
#include "mlir/IR/Matchers.h"

using namespace mlir;

namespace {

struct KokkosMemorySpaceRewriter : public OpRewritePattern<scf::ParallelOp> {
  using OpRewritePattern<scf::ParallelOp>::OpRewritePattern;

  KokkosMemorySpaceRewriter (MLIRContext *context)
      : OpRewritePattern(context) {}

  LogicalResult matchAndRewrite(scf::ParallelOp op, PatternRewriter &rewriter) const override {
    return failure();
  }
};

} // namespace

void mlir::populateKokkosMemorySpaceAssignmentPatterns(RewritePatternSet &patterns)
{
  //patterns.add<KokkosMemorySpaceRewriter>(patterns.getContext());
}

