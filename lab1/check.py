import argparse
import numpy as np

p = argparse.ArgumentParser()
p.add_argument("--a", default="A.txt")
p.add_argument("--b", default="B.txt")
p.add_argument("--result", default="result.txt")
args = p.parse_args()

def read_matrix(filename):
    with open(filename, encoding="utf-8") as f:
        n = int(f.readline())
        values = np.loadtxt(f, dtype=np.float64, ndmin=2)
    if values.shape != (n, n):
        raise ValueError(f"Invalid shape in {filename}: {values.shape}")
    return values

a = read_matrix(args.a)
b = read_matrix(args.b)
c = read_matrix(args.result)
expected = a @ b
if np.allclose(expected, c, rtol=1e-9, atol=1e-7):
    print("PASS: NumPy verification succeeded")
else:
    print("FAIL: matrices differ, max error:", np.max(np.abs(expected - c)))
    raise SystemExit(1)
