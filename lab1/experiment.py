import argparse
import csv
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

p = argparse.ArgumentParser(description="Sequential matrix multiplication benchmarks")
p.add_argument("--exe", default="matrix.exe" if os.name == "nt" else "./matrix")
p.add_argument("--sizes", type=int, nargs="+", default=[200, 400, 800, 1200, 1600, 2000])
p.add_argument("--repeats", type=int, default=1)
args = p.parse_args()
if args.repeats < 1 or any(n < 1 for n in args.sizes):
    p.error("Sizes and repeats must be positive")

Path("results").mkdir(exist_ok=True)
rows = []
for n in args.sizes:
    subprocess.run([sys.executable, "generate.py", str(n)], check=True)
    times = []
    for rep in range(args.repeats):
        proc = subprocess.run([args.exe], check=True, capture_output=True, text=True)
        match = re.search(r"time_sec=([0-9.]+)", proc.stdout)
        if not match:
            raise RuntimeError(proc.stdout)
        times.append(float(match.group(1)))
        print(f"N={n}, repeat={rep+1}: {times[-1]:.6f} sec", flush=True)
    subprocess.run([sys.executable, "check.py"], check=True)
    rows.append({"N": n, "time_sec": round(sum(times)/len(times), 6),
                 "operations": 2*n**3, "memory_bytes": 3*n*n*8,
                 "verified": "PASS", "repeats": args.repeats})

with open("results/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 4.8))
plt.plot([r["N"] for r in rows], [r["time_sec"] for r in rows], marker="o")
plt.title("Sequential matrix multiplication")
plt.xlabel("Matrix size N")
plt.ylabel("Time (seconds)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("results/time_vs_size.png", dpi=160)
plt.close()

report = Path("README.md")
text = report.read_text(encoding="utf-8")
start = "<!-- RESULTS_START -->"
end = "<!-- RESULTS_END -->"
header = "| N | Время, с | Операций (оценка) | Память трёх матриц, байт | Проверка |\n|---:|---:|---:|---:|:---:|\n"
body = "".join(f'| {r["N"]} | {r["time_sec"]:.6f} | {r["operations"]} | {r["memory_bytes"]} | {r["verified"]} |\n' for r in rows)
block = ("\n**Условия измерений:** " + platform.platform() + "; Python " + platform.python_version() + ". "
         + f"Каждый размер: {args.repeats} запуск(ов); указано среднее время. "
         + "Время измерено только для умножения, без чтения и записи файлов.\n\n"
         + header + body + "\n![График времени](results/time_vs_size.png)\n\n"
         + "**Вывод по эксперименту:** при увеличении N время умножения растёт; "
         + "теоретическая сложность алгоритма O(N³). Точные значения зависят от компьютера и компилятора.\n")
report.write_text(text.split(start)[0] + start + "\n" + block + end + text.split(end)[1], encoding="utf-8")
print("Saved results/results.csv, results/time_vs_size.png and updated README.md")
