# Semgrep Consolidator - Built during work 🏗️

This repository contains a Python script to run Semgrep scans on various programming languages and consolidate the results into a single SARIF report.

## Installation

1. Install Semgrep:
    ```sh
    pip install semgrep
    ```

2. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/semgrep-consolidator.git
    cd semgrep-consolidator
    ```

## Usage

1. Run the main script:
    ```sh
    python main.py
    ```

2. Follow the prompts to enter *language keywords* and project source paths.

3. After entering all the desired keywords and paths, provide a *project name* for the reports directory.

## Supported Languages and Configurations

The script supports the following languages and configurations: You just need to enter the language when the script prompts you to. Eg: Java.

- **Java**: `p/default`, `p/java`, `p/owasp-top-ten`, `p/cwe-top-25`, `p/findsecbugs`
- **Node**: `p/default`, `p/owasp-top-ten`, `p/cwe-top-25`, `p/nodejs`, `p/insecure-transport-jsnode`, `p/eslint`
- **Python (Flask)**: `p/bandit`, `p/default`, `p/flask`, `p/python`, `p/secure-defaults`, `p/owasp-top-ten`, `p/cwe-top-25`
- **Python (Django)**: `p/bandit`, `p/default`, `p/django`, `p/python`, `p/secure-defaults`, `p/owasp-top-ten`, `p/cwe-top-25`
- **PHP**: `p/default`, `p/owasp-top-ten`, `p/cwe-top-25`, `p/php`, `p/php-laravel`, `p/phpcs-security-audit`
- **React**: `p/default`, `p/react`, `p/typescript`, `p/javascript`, `p/eslint`
- **Angular**: `p/default`, `p/angular`, `p/typescript`, `p/javascript`, `p/eslint`

```bash
$ python main.py
Enter a language keyword (e.g., 'Java', 'React', 'Angular') or 'done' to finish: Java
Enter the project source path for 'java': /path/to/java/project
Added 'java' with path '/path/to/java/project' to the list.

Enter a language keyword (e.g., 'Java', 'React', 'Angular') or 'done' to finish: react
Enter the project source path for 'react': /path/to/react/project
Added 'react' with path '/path/to/react/project' to the list.

Enter a language keyword (e.g., 'Java', 'React', 'Angular') or 'done' to finish: done

Enter the project name to create a directory for the reports: my_project

Generating SARIF report for config: p/default
Running Semgrep with config: p/default, project path: /path/to/java/project
Generating SARIF report for config: p/java
Running Semgrep with config: p/java, project path: /path/to/java/project
Generating SARIF report for config: p/owasp-top-ten
Running Semgrep with config: p/owasp-top-ten, project path: /path/to/java/project
Generating SARIF report for config: p/cwe-top-25
Running Semgrep with config: p/cwe-top-25, project path: /path/to/java/project
Generating SARIF report for config: p/findsecbugs
Running Semgrep with config: p/findsecbugs, project path: /path/to/java/project

Consolidating reports...
Saving consolidated report to: my_project/consolidated_report_java.sarif
Consolidated SARIF report for 'java' saved to: my_project/consolidated_report_java.sarif

Generating SARIF report for config: p/default
Running Semgrep with config: p/default, project path: /path/to/react/project
Generating SARIF report for config: p/react
Running Semgrep with config: p/react, project path: /path/to/react/project
Generating SARIF report for config: p/typescript
Running Semgrep with config: p/typescript, project path: /path/to/react/project
Generating SARIF report for config: p/javascript
Running Semgrep with config: p/javascript, project path: /path/to/react/project
Generating SARIF report for config: p/eslint
Running Semgrep with config: p/eslint, project path: /path/to/react/project

Consolidating reports...
Saving consolidated report to: my_project/consolidated_report_react.sarif
Consolidated SARIF report for 'react' saved to: my_project/consolidated_report_react.sarif

Cleaning up temporary SARIF files...

All reports have been consolidated and saved.
```