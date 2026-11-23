import argparse
import random
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("size", type=int)
parser.add_argument("--seed", type=int, default=42)
args = parser.parse_args()
if args.size <= 0:
    parser.error("size must be positive")
rng = random.Random(args.seed)
for name in ("A.txt", "B.txt"):
    with Path(name).open("w", encoding="utf-8") as f:
        f.write(f"{args.size}\n")
        for _ in range(args.size):
            f.write(" ".join(str(rng.randint(-5, 5)) for _ in range(args.size)) + "\n")
print(f"Generated {args.size}x{args.size} matrices")
