import torch
import torch_directml

print(f"Torch version: {torch.__version__}")
dml = torch_directml.device()
print(f"DirectML device: {dml}")

try:
    x = torch.tensor([1.0, 2.0]).to(dml)
    y = x * 2
    print(f"Computation on DirectML: {y}")
    print("SUCCESS")
except Exception as e:
    print(f"FAILURE: {e}")
