import argparse
import os
import statistics
from multiprocessing import Pool
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
benchmarks_dir = root_dir / "benchmarks"
default_output_fname = str(
    root_dir / ("out_baseline_" + date.today().strftime("%Y%m%d") + ".csv")
)

parser = argparse.ArgumentParser(description="Run CrossHair benchmarks")
parser.add_argument(
    "-t", "--timeout", type=int, help="Maximum condition checking timeout",
    default=10 * 60
)
parser.add_argument(
    "-p", "--parallel",
    type=int,
    help="Amount of parallelism",
    default=max(1, (os.cpu_count() or 1) - 2)
)
parser.add_argument(
    "-o", "--output", help="Csv file for benchmark data", default=default_output_fname
)
parser.add_argument(
    "-r", "--repeat",
    type=int,
    help="Run each benchmark this many times and report the median duration "
         "(plus a per-sample sidecar). Use >1 to gauge timing variance.",
    default=1,
)
parser.add_argument(
    "paths",
    nargs="*",
    help="Optional benchmark files or directories to run. A directory is "
         "expanded to its crosshair_*.py files. Defaults to the whole suite.",
)
args = parser.parse_args()

repeat = max(1, args.repeat)

if Path(args.output).exists():
    print("Output file already exists. Please remove it first.")
    sys.exit(1)

timeout = args.timeout
basecmd = [
    sys.executable,
    "-m",
    "crosshair",
    "check",
    f"--per_condition_timeout={timeout}",
    f"--per_path_timeout={timeout ** 0.5}",
]

def run_once(cmd: list) -> tuple[float, int, str]:
    t0 = time.monotonic()
    proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output = str(proc.communicate()[0])
    duration = time.monotonic() - t0
    return (duration, proc.returncode, output)

def run_file(benchmark_file: Path) -> tuple[str, list, int, str]:
    benchmark_name = "/".join(benchmark_file.parts[-2:])
    cmd = basecmd + [str(benchmark_file)]
    durations = []
    code = 0
    last_output = ""
    for _ in range(repeat):
        duration, code, last_output = run_once(cmd)
        durations.append(duration)
    # Report the median run as the representative (code, duration) so the CSV
    # stays in the 3-column format the analyzer expects.  The exit code should
    # be stable across repeats for a given contract; we keep the last one.
    median = statistics.median(durations)
    samples = " ".join(f"{d:.3f}" for d in durations)
    trace = (
        f"Run: {' '.join(cmd)}\n"
        f"Durations: {samples}\nMedian: {median}\nOutput: {last_output}\n"
    )
    return (benchmark_name, durations, code, trace)

def collect_benchmark_files(paths):
    if not paths:
        return sorted(benchmarks_dir.glob("*/crosshair_*.py"))
    files = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(p.glob("crosshair_*.py"))
        else:
            files.append(p)
    return sorted(set(files))

if __name__ == '__main__':
    timings = {}
    pool = Pool(args.parallel)
    benchmark_files = collect_benchmark_files(args.paths)
    for benchmark_name, durations, code, trace in pool.imap_unordered(run_file, benchmark_files):
        timings[benchmark_name] = (code, durations)
        print()
        print(trace)


    # Main CSV: name,code,median_duration  (unchanged 3-column format).
    with open(args.output, "w") as fh:
        for name, (code, durations) in sorted(timings.items()):
            fh.write(f"{name},{code},{statistics.median(durations)}\n")

    # When repeating, also emit a per-sample sidecar with the full distribution.
    if repeat > 1:
        sidecar = args.output + ".samples.csv"
        with open(sidecar, "w") as fh:
            for name, (code, durations) in sorted(timings.items()):
                lo, hi = min(durations), max(durations)
                med = statistics.median(durations)
                allsamples = " ".join(f"{d:.3f}" for d in durations)
                fh.write(f"{name},{code},{lo},{med},{hi},{allsamples}\n")
        print(f"Per-sample distribution written to {sidecar}")

    print()
    print("Benchmarks complete")
