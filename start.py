#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess

# 1. Enter the full absolute paths of the scripts you want to run sequentially here
scripts = [
    "/mnt/nvme1/fmy/LiveVQApro/run.py",
    "/mnt/nvme1/fmy/LiveVQApro/ranking/Model_ranking.py",
    "/mnt/nvme1/fmy/LiveVQApro/qa_makers/main.py",
    "/mnt/nvme1/fmy/LiveVQApro/test_set/model_filter.py",
    "/mnt/nvme1/fmy/LiveVQApro/qa_makers_mh/multihop_generator.py"
]

def run_scripts(scripts_list):
    """
    Runs each script in the list sequentially, printing their stdout/stderr in real-time.
    If a script returns a non-zero exit code, subsequent scripts are stopped, and the program exits with that code.
    """
    for script_path in scripts_list:
        print(f"\n=== Running: {script_path} ===\n")
        # Execute the script using the current Python interpreter
        proc = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line-buffered
        )
        # Read and print subprocess output in real-time
        for line in proc.stdout:
            print(line, end='')  # Already includes newline

        retcode = proc.wait()
        if retcode != 0:
            print(f"\n*** Script {script_path} terminated with exit code {retcode}, stopping further execution ***")
            sys.exit(retcode)

    print("\n=== All scripts executed successfully ===")

if __name__ == "__main__":
    run_scripts(scripts)