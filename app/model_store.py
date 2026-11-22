"""Prepares and loads the quantized Detoxify model from persistent storage.

`python -m model_store` (run by entrypoint.sh before the server starts) makes sure the
quantized model exists in MODEL_DIR. The original fp32 weights are only loaded in that
short-lived process, so the server itself only ever holds the small int8 model.
"""
import gc
import os
import platform
import warnings

MODEL_DIR = os.getenv("MODEL_DIR", "/models")
# Cache the original checkpoint on the volume too, so it is downloaded only once.
os.environ.setdefault("TORCH_HOME", os.path.join(MODEL_DIR, "torch"))

import torch  # noqa: E402
from torch import nn  # noqa: E402

warnings.filterwarnings("ignore", category=DeprecationWarning)


def _engine() -> str:
    # Packed int8 weights are tied to the CPU backend they were built with.
    return "fbgemm" if platform.machine().lower() in ("x86_64", "amd64") else "qnnpack"


def model_path() -> str:
    version = torch.__version__.split("+")[0]
    return os.path.join(MODEL_DIR, f"detoxify-multilingual-int8-torch{version}-{_engine()}.pt")


def prepare() -> str:
    """Build the quantized model into MODEL_DIR unless it is already there."""
    path = model_path()
    if os.path.exists(path):
        print(f"Model already present: {path}", flush=True)
        return path

    print("Model not found, downloading and quantizing (one-time step)...", flush=True)
    from detoxify import Detoxify
    from torch.ao.quantization import (
        default_dynamic_qconfig,
        float_qparams_weight_only_qconfig,
        quantize_dynamic,
    )

    os.makedirs(MODEL_DIR, exist_ok=True)
    torch.backends.quantized.engine = _engine()
    detox = Detoxify("multilingual")
    detox.model = quantize_dynamic(
        detox.model,
        {nn.Linear: default_dynamic_qconfig, nn.Embedding: float_qparams_weight_only_qconfig},
        dtype=torch.qint8,
    )
    gc.collect()
    # Write to a temp file and rename, so a crash or a second replica never sees a partial file.
    tmp = f"{path}.{os.getpid()}.tmp"
    torch.save(detox, tmp)
    os.replace(tmp, path)
    print(f"Saved {path}", flush=True)
    return path


def load():
    """Load the quantized model, preparing it first if needed (e.g. local runs)."""
    path = prepare()
    torch.backends.quantized.engine = _engine()
    # The file is written by prepare() on a volume we control, never user-supplied.
    model = torch.load(path, weights_only=False)
    gc.collect()
    return model


if __name__ == "__main__":
    prepare()
