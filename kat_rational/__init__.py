from importlib import import_module

def _try(path, *names):
    """import path and return requested names or None on failure"""
    try:
        mod = import_module(path, __package__)
        return [getattr(mod, n) for n in names]
    except Exception:                # anything (ImportError, OSError, ...)
        return [None] * len(names)

# ────────────────────────────────────────────────────────────────────────────────
# 1-D group implementation
# ────────────────────────────────────────────────────────────────────────────────
RationalTriton1DGroup, KAT_Group = _try(
    ".kat_1dgroup_triton",
    "RationalTriton1DGroup", "KAT_Group"
)

# fall-back to the pure-PyTorch version if Triton path is unavailable
if KAT_Group is None:
    from .kat_1dgroup_torch import KAT_Group_Torch as KAT_Group
    RationalTriton1DGroup = None     # still export the symbol

# ────────────────────────────────────────────────────────────────────────────────
# 2-D implementation (CUDA only, so also optional)
# ────────────────────────────────────────────────────────────────────────────────
[KAT_Group2D] = _try(".kat_2dgroup_triton", "KAT_Group2D")

__all__ = ["KAT_Group", "KAT_Group2D", "RationalTriton1DGroup"]
