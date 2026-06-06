import subprocess
import sys


def run_module(module_name: str, python_executable: str) -> None:
    """Run a Python module and stop the pipeline if it fails."""
    print(f"\nRunning module: {module_name}")

    result = subprocess.run(
        [python_executable, "-m", module_name],
        check=False,
        capture_output=True,
        text=True,
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Pipeline failed while running {module_name}")


def main():
    python_executable = sys.executable

    modules = [
        "src.ingestion.generate_invoices",
        "src.ingestion.load_invoices",
        "src.transform.build_price_history",
        "src.monitoring.detect_price_alerts",
    ]

    print("Starting hospitality procurement monitoring pipeline...")

    for module_name in modules:
        run_module(module_name, python_executable)

    print("\nPipeline completed successfully.")
    print("Outputs created:")
    print("- PostgreSQL tables: raw_invoices, price_history, price_alerts")
    print("- Alerts CSV: outputs/price_alerts.csv")


if __name__ == "__main__":
    main()