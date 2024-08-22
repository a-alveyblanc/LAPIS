# -*- Python -*-

import os
import platform
import re
import subprocess
import tempfile

import lit.formats
import lit.util

from lit.llvm import llvm_config
from lit.llvm.subst import ToolSubst
from lit.llvm.subst import FindTool

# Configuration file for the 'lit' test runner.

# name: The name of this test suite.
config.name = "MLIR"

config.test_format = lit.formats.ShTest(not llvm_config.use_lit_shell)

# suffixes: A list of file extensions to treat as test files.
config.suffixes = [
    ".td",
    ".mlir",
    ".toy",
    ".ll",
    ".tc",
    ".py",
    ".yaml",
    ".test",
    ".pdll",
    ".c",
]

# test_source_root: The root path where tests are located.
config.test_source_root = os.path.dirname(__file__)

# test_exec_root: The root path where tests should be run.
config.test_exec_root = os.path.join(config.mlir_obj_root, "test")

config.substitutions.append(("%PATH%", config.environment["PATH"]))
config.substitutions.append(("%shlibext", config.llvm_shlib_ext))
config.substitutions.append(("%mlir_src_root", config.mlir_src_root))
config.substitutions.append(("%host_cxx", config.host_cxx))
config.substitutions.append(("%host_cc", config.host_cc))


# Searches for a runtime library with the given name and returns a tool
# substitution of the same name and the found path.
# Correctly handles the platforms shared library directory and naming conventions.
def add_runtime(name):
    path = ""
    for prefix in ["", "lib"]:
        path = os.path.join(
            config.llvm_shlib_dir, f"{prefix}{name}{config.llvm_shlib_ext}"
        )
        if os.path.isfile(path):
            break
    return ToolSubst(f"%{name}", path)


llvm_config.with_system_environment(["HOME", "INCLUDE", "LIB", "TMP", "TEMP"])

llvm_config.use_default_substitutions()

# excludes: A list of directories to exclude from the testsuite. The 'Inputs'
# subdirectories contain auxiliary inputs for various tests in their parent
# directories.
config.excludes = [
    "Inputs",
    "CMakeLists.txt",
    "README.txt",
    "LICENSE.txt",
    "lit.cfg.py",
    "lit.site.cfg.py",
]

# Tweak the PATH to include the tools dir.
llvm_config.with_environment("PATH", config.mlir_tools_dir, append_path=True)
llvm_config.with_environment("PATH", config.llvm_tools_dir, append_path=True)

tool_dirs = [config.mlir_tools_dir, config.llvm_tools_dir]
tools = [
    "mlir-tblgen",
    "mlir-translate",
    "mlir-lsp-server",
    "mlir-capi-execution-engine-test",
    "mlir-capi-ir-test",
    "mlir-capi-llvm-test",
    "mlir-capi-pass-test",
    "mlir-capi-pdl-test",
    "mlir-capi-quant-test",
    "mlir-capi-sparse-tensor-test",
    "mlir-capi-transform-test",
    "mlir-cpu-runner",
    add_runtime("mlir_runner_utils"),
    add_runtime("mlir_c_runner_utils"),
    add_runtime("mlir_async_runtime"),
    add_runtime("mlir_float16_utils"),
    "mlir-linalg-ods-yaml-gen",
    "mlir-reduce",
    "mlir-pdll",
    "not",
]

if config.enable_spirv_cpu_runner:
    tools.extend(
        ["mlir-spirv-cpu-runner", add_runtime("mlir_test_spirv_cpu_runner_c_wrappers")]
    )

if config.enable_vulkan_runner:
    tools.extend([add_runtime("vulkan-runtime-wrappers")])

if config.enable_rocm_runner:
    tools.extend([add_runtime("mlir_rocm_runtime")])

if config.enable_cuda_runner:
    tools.extend([add_runtime("mlir_cuda_runtime")])

# The following tools are optional
tools.extend(
    [
        ToolSubst("toyc-ch1", unresolved="ignore"),
        ToolSubst("toyc-ch2", unresolved="ignore"),
        ToolSubst("toyc-ch3", unresolved="ignore"),
        ToolSubst("toyc-ch4", unresolved="ignore"),
        ToolSubst("toyc-ch5", unresolved="ignore"),
        ToolSubst("toyc-ch6", unresolved="ignore"),
        ToolSubst("toyc-ch7", unresolved="ignore"),
        ToolSubst('transform-opt-ch2', unresolved='ignore'),
        ToolSubst('transform-opt-ch3', unresolved='ignore'),
        ToolSubst("%mlir_lib_dir", config.mlir_lib_dir, unresolved="ignore"),
        ToolSubst("%mlir_src_dir", config.mlir_src_root, unresolved="ignore"),
    ]
)

python_executable = config.python_executable
# Python configuration with sanitizer requires some magic preloading. This will only work on clang/linux.
# TODO: detect Darwin/Windows situation (or mark these tests as unsupported on these platforms).
if "asan" in config.available_features and "Linux" in config.host_os:
    python_executable = f"LD_PRELOAD=$({config.host_cxx} -print-file-name=libclang_rt.asan-{config.host_arch}.so) {config.python_executable}"
# On Windows the path to python could contains spaces in which case it needs to be provided in quotes.
# This is the equivalent of how %python is setup in llvm/utils/lit/lit/llvm/config.py.
elif "Windows" in config.host_os:
    python_executable = '"%s"' % (python_executable)
tools.extend(
    [
        ToolSubst("%PYTHON", python_executable, unresolved="ignore"),
    ]
)

if "MLIR_OPT_CHECK_IR_ROUNDTRIP" in os.environ:
    tools.extend(
        [
            ToolSubst("mlir-opt", "mlir-opt --verify-roundtrip", unresolved="fatal"),
        ]
    )
else:
    tools.extend(["mlir-opt"])

llvm_config.add_tool_substitutions(tools, tool_dirs)


# FileCheck -enable-var-scope is enabled by default in MLIR test
# This option avoids to accidentally reuse variable across -LABEL match,
# it can be explicitly opted-in by prefixing the variable name with $
config.environment["FILECHECK_OPTS"] = "-enable-var-scope --allow-unused-prefixes=false"

# Add the python path for both the source and binary tree.
# Note that presently, the python sources come from the source tree and the
# binaries come from the build tree. This should be unified to the build tree
# by copying/linking sources to build.
if config.enable_bindings_python:
    llvm_config.with_environment(
        "PYTHONPATH",
        [
            os.path.join(config.mlir_obj_root, "python_packages", "mlir_core"),
            os.path.join(config.mlir_obj_root, "python_packages", "mlir_test"),
        ],
        append_path=True,
    )

if config.enable_assertions:
    config.available_features.add("asserts")
else:
    config.available_features.add("noasserts")


def have_host_jit_feature_support(feature_name):
    mlir_cpu_runner_exe = lit.util.which("mlir-cpu-runner", config.mlir_tools_dir)

    if not mlir_cpu_runner_exe:
        return False

    try:
        mlir_cpu_runner_cmd = subprocess.Popen(
            [mlir_cpu_runner_exe, "--host-supports-" + feature_name],
            stdout=subprocess.PIPE,
        )
    except OSError:
        print("could not exec mlir-cpu-runner")
        return False

    mlir_cpu_runner_out = mlir_cpu_runner_cmd.stdout.read().decode("ascii")
    mlir_cpu_runner_cmd.wait()

    return "true" in mlir_cpu_runner_out


if have_host_jit_feature_support("jit"):
    config.available_features.add("host-supports-jit")

if config.run_cuda_tests:
    config.available_features.add("host-supports-nvptx")

if config.run_rocm_tests:
    config.available_features.add("host-supports-amdgpu")
