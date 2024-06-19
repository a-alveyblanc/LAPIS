import torch
from torch import Tensor
import torch_mlir
from kokkos_mlir.linalg_kokkos_backend import KokkosBackend
from torch import nn


class Adder(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        return a + b


def main():
    a = 5 * torch.ones((5, 5))
    b = torch.ones((5, 5))

    m = Adder()
    m.train(False)

    mlir_module = torch_mlir.compile(
        m, (a, b), output_type=torch_mlir.OutputType.LINALG_ON_TENSORS
    )

    backend = KokkosBackend.KokkosBackendLinalgOnTensorsBackend(dump_mlir=True)
    k_backend = backend.compile(mlir_module)

    c = k_backend.forward(a, b)
    print("c from kokkos")
    print(c)

    print("c from pytorch")
    print(m.forward(a, b))

if __name__ == "__main__":
    main()