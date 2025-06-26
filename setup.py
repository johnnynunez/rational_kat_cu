# setup.py
import glob
from pathlib import Path
from setuptools import setup
from setuptools.command.build_ext import build_ext


def get_extensions():
    """
    Lazily import torch after it is guaranteed to be available
    and return (ext_modules, cmdclass).
    """
    try:
        from torch.utils.cpp_extension import BuildExtension, CUDAExtension
    except ImportError as e:
        raise RuntimeError(
            "PyTorch must be installed to build the C++/CUDA extension.\n"
            "Try:  pip install torch --index-url https://download.pytorch.org/whl/cu121"
        ) from e

    sources = glob.glob("src/*.cpp") + glob.glob("src/*.cu")

    ext_modules = [
        CUDAExtension(
            name="kat_rational._cuda",
            sources=sources,
            extra_compile_args={
                "cxx": ["-O3"],
                "nvcc": ["-O3", "-use_fast_math"],
            },
        )
    ]
    return ext_modules, {"build_ext": BuildExtension}


ext_modules, cmdclass = get_extensions()

setup(
    name="kat_rational",
    version="0.4",
    author="adamdad",
    author_email="yxy_adadm@qq.com",
    description="CUDA-optimised group-wise rational function for KAT",
    long_description=(
        "A PyTorch C++/CUDA extension that provides fast group-wise rational "
        "functions used in the *kat* project."
    ),
    python_requires=">=3.8",
    install_requires=["torch>=2.0",  "triton", "numpy"],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
)
