# setup.py
import glob
from setuptools import setup

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
    cmdclass = {"build_ext": BuildExtension}
    return ext_modules, cmdclass

ext_modules, cmdclass = get_extensions()

setup(
    ext_modules=ext_modules,
    cmdclass=cmdclass,
)