import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "generate_customers.py",
    "generate_sources.py",
    "generate_pipelines.py",
    "generate_assets.py",
    "generate_checks.py",
    "generate_pipeline_runs.py",
    "generate_quality_results.py",
]

def main():
    for script in SCRIPTS:
        path = SCRIPT_DIR / script
        print(f"\n=== Running {script} ===")
        subprocess.run(
            [sys.executable, str(path)],
            check=True,
            cwd=SCRIPT_DIR.parent
        )

    print("\nSynthetic dataset generation completed.")

if __name__ == "__main__":
    main()
