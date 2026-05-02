# Test report generator
# Runs pytest and produces HTML report + summary

import subprocess
import sys
import os
import json
from datetime import datetime


def run_tests(
    test_path:   str  = ".",
    report_dir:  str  = "reports",
    verbose:     bool = True,
    markers:     str  = "",
    capture:     str  = "no",
) -> dict:
    """
    Run pytest and generate HTML + JSON reports.

    Returns dict with:
        passed, failed, errors, skipped, duration, report_path
    """
    os.makedirs(report_dir, exist_ok=True)

    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = os.path.join(report_dir, f"report_{timestamp}.html")
    json_report = os.path.join(report_dir, f"report_{timestamp}.json")

    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        f"--html={html_report}",
        "--self-contained-html",
        f"--json-report",
        f"--json-report-file={json_report}",
        f"--capture={capture}",
        "--tb=short",
    ]

    if verbose:
        cmd.append("-v")

    if markers:
        cmd.extend(["-m", markers])

    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, capture_output=False)

    # Parse JSON report if available
    summary = {
        "passed":      0,
        "failed":      0,
        "errors":      0,
        "skipped":     0,
        "duration":    0.0,
        "report_path": html_report,
        "return_code": result.returncode,
    }

    if os.path.exists(json_report):
        with open(json_report) as f:
            data = json.load(f)
        summary.update({
            "passed":   data.get("summary", {}).get("passed",  0),
            "failed":   data.get("summary", {}).get("failed",  0),
            "errors":   data.get("summary", {}).get("error",   0),
            "skipped":  data.get("summary", {}).get("skipped", 0),
            "duration": data.get("duration", 0.0),
        })

    print(f"\n{'='*60}")
    print(f"RESULTS: {summary['passed']} passed | "
          f"{summary['failed']} failed | "
          f"{summary['errors']} errors | "
          f"{summary['skipped']} skipped")
    print(f"Duration:   {summary['duration']:.2f}s")
    print(f"Report:     {html_report}")
    print(f"{'='*60}\n")

    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run tests and generate report")
    parser.add_argument("--path",    default=".",        help="Test path")
    parser.add_argument("--dir",     default="reports",  help="Report directory")
    parser.add_argument("--markers", default="",         help="pytest markers")
    args = parser.parse_args()

    summary = run_tests(test_path=args.path, report_dir=args.dir, markers=args.markers)
    sys.exit(0 if summary["return_code"] == 0 else 1)
