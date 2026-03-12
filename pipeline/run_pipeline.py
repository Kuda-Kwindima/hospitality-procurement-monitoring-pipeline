from pathlib import Path
import subprocess
import sys


def run_script(script_path: Path, python_executable: str) -> None:
    """Run a Python script and stop the pipeline if it fails."""
    print(f"\nRunning: {script_path}")
    result = subprocess.run(
        [python_executable, str(script_path)],
        check=False,
        capture_output=True,
        text=True,
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Pipeline failed while running {script_path.name}")


def main():
    project_root = Path(__file__).resolve().parents[1]

    python_executable = sys.executable

    scripts = [
        project_root / "src" / "ingestion" / "generate_invoices.py",
        project_root / "src" / "ingestion" / "load_invoices.py",
        project_root / "src" / "transform" / "build_price_history.py",
        project_root / "src" / "monitoring" / "detect_price_alerts.py",
    ]

    print("Starting hospitality procurement monitoring pipeline...")

    for script in scripts:
        run_script(script, python_executable)

    print("\nPipeline completed successfully.")
    print("Outputs created:")
    print(f"- Database: {project_root / 'db' / 'procurement.db'}")
    print(f"- Alerts CSV: {project_root / 'outputs' / 'price_alerts.csv'}")


if __name__ == "__main__":
    main()