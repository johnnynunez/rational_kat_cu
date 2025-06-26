# setup.py (Corregido)
import glob
from setuptools import setup, find_packages  # Importar find_packages


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

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kat_rational",
    version="0.4",
    author="adamdad",
    author_email="yxy_adadm@qq.com",
    description="CUDA-optimised group-wise rational function for KAT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Adamdad/rational_kat_cu",

    packages=find_packages(exclude=("tests", "example")),

    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0",
        "numpy>=1.26.4",
        # Instalación condicional de Triton
        'triton>=2.1.0; sys_platform != "win32"',
        'triton-windows>=2.1.0; sys_platform == "win32"',
    ],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
)