import subprocess
import json
import os
from pathlib import Path

def run_semgrep(config, project_src_path, output_file):
    print(f"Running Semgrep with config: {config}, project path: {project_src_path}")
    result = subprocess.run(
        ["semgrep", "--config", config, "--sarif", "--sarif-output", output_file, project_src_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error running Semgrep with config {config}: {result.stderr}")
        return None
    with open(output_file, 'r') as f:
        return json.load(f)

def consolidate_reports(reports):
    consolidated = {
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "version": "2.1.0",
        "runs": []
    }

    all_results = []
    for report in reports:
        for run in report.get("runs", []):
            for result in run.get("results", []):
                if result not in all_results:
                    print("\n==========")
                    print(result)
                    all_results.append(result)

    consolidated["runs"].append({
        "tool": {
            "driver": {
                "name": "semgrep",
                "informationUri": "https://semgrep.dev"
            }
        },
        "results": all_results
    })

    return consolidated

def save_consolidated_report(report, output_path):
    print(f"Saving consolidated report to: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

def main():

    keyword_to_configs = {
        "java": ["p/default","p/java", "p/owasp-top-ten", "p/cwe-top-25", "p/findsecbugs"],
        "node": ["p/default", "p/owasp-top-ten", "p/cwe-top-25","p/nodejs","p/insecure-transport-jsnode", "p/eslint"],
        "python-flask": ["p/bandit","p/default","p/flask","p/python","p/secure-defaults", "p/owasp-top-ten", "p/cwe-top-25"],
        "python-django": ["p/bandit","p/default","p/django","p/python","p/secure-defaults", "p/owasp-top-ten", "p/cwe-top-25"],
        "php": ["p/default", "p/owasp-top-ten", "p/cwe-top-25","p/php", "p/php-laravel", "p/phpcs-security-audit"],
        "react": ["p/default","p/react", "p/typescript", "p/javascript", "p/eslint"],
        "angular": ["p/default","p/angular", "p/typescript", "p/javascript", "p/eslint"]
    }

    selected_keywords = {}
    
    while True:

        keyword = input("Enter a language keyword (e.g., 'Java', 'React', 'Angular') or 'done' to finish: ").strip().lower()
        
        if keyword == 'done':
            break

        if keyword in keyword_to_configs:
            # Project path input for the selected language
            project_src_path = input(f"Enter the project source path for '{keyword}': ")
            if not os.path.exists(project_src_path):
                print(f"The provided path for '{keyword}' does not exist. Please try again.")
                continue

            # Store the configs and project path
            selected_keywords[keyword] = {
                "configs": keyword_to_configs[keyword],
                "path": project_src_path
            }
            print(f"Added '{keyword}' with path '{project_src_path}' to the list.")
        else:
            print("Invalid keyword. Please try again.")

    if not selected_keywords:
        print("No valid configurations were selected. Exiting.")
        return

    # Project name input
    project_name = input("Enter the project name to create a directory for the reports: ").strip()
    reports_dir = Path(f"./{project_name}")
    reports_dir.mkdir(exist_ok=True)

    for keyword, info in selected_keywords.items():
        configs = info["configs"]
        project_src_path = info["path"]

        all_reports = []

        for config in configs:
            output_file = reports_dir / f"{keyword}_{config.replace('/', '_')}_report.sarif"
            print(f"Generating SARIF report for config: {config}")
            report = run_semgrep(config, project_src_path, output_file)
            if report:
                all_reports.append(report)

        if all_reports:
            consolidated_report = consolidate_reports(all_reports)
            output_path = reports_dir / f"consolidated_report_{keyword}.sarif"
            save_consolidated_report(consolidated_report, output_path)
            print(f"Consolidated SARIF report for '{keyword}' saved to: {output_path}")

        # Clean up temporary SARIF files after consolidation
        for file in reports_dir.glob(f"{keyword}_*_report.sarif"):
            file.unlink()

if __name__ == "__main__":
    main()