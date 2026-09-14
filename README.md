# Shift Left Security — Task Management Web App

This is the practical web application for the session:

**Shift Left Security: Building Applications That Are Secure by Design in the Age of AI**

The application is intentionally vulnerable. The goal is to build it first, identify security weaknesses at the appropriate SDLC stages, demonstrate the attacks in a local lab, and then remediate them.

## Stack

- Python
- Flask
- SQLite
- HTML/CSS
- Semgrep
- SonarQube (optional for the demo)

## Application flow

User -> Browser -> Flask Web App -> SQLite Database

The application supports:

- Register
- Login
- Create task
- View task
- Logout

## Deliberate vulnerabilities

This version contains weaknesses for the security demonstration:

1. SQL injection in the login query
2. Broken Object Level Authorization / IDOR in task viewing
3. Hardcoded Flask secret
4. Passwords stored in plaintext
5. Debug mode enabled

These are intentionally included for the local classroom demonstration.

## Run the application

### Windows

Open PowerShell in this directory:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

## Demo setup

Create two accounts:

- alice
- bob

Log in as Alice and create a task.

Then log in as Bob and change the task ID in the URL.

For example:

```text
http://127.0.0.1:5000/tasks/1
```

The vulnerable application does not verify that task 1 belongs to Bob.

This demonstrates broken object-level authorization / IDOR.

## SQL injection demonstration

Use only this local demo application.

On the login page, the username field can be tested with:

```text
' OR '1'='1' --
```

The point of the demonstration is not the payload itself. The important lesson is why string concatenation creates the vulnerability and why parameterized queries prevent it.

## Semgrep

From the project directory:

```bash
semgrep --config p/owasp-top-ten .
```

If the registry configuration is unavailable, use a local ruleset instead.

## SonarQube

Run the application code through SonarQube after the initial Semgrep demonstration.

The goal is to show that automated tools can identify security/code-quality problems before the code reaches production.

## Secure remediation

The secure version should:

- use parameterized database queries
- hash passwords with a password-hashing function
- use a secret from an environment variable
- verify task ownership before returning a task
- disable debug mode in production
- add appropriate authentication/session protections
- add dependency/security scanning to CI

## Mapping to the presentation

| Presentation stage | Demo action |
|---|---|
| Requirements | Define security requirements |
| Threat modeling | Apply STRIDE to the app |
| Technology selection | Check dependencies/CVEs |
| AI-assisted development | Compare weak vs security-aware prompts |
| Coding | Show vulnerable code |
| OWASP Top 10 | Map findings to categories |
| SAST | Run Semgrep/SonarQube |
| Testing | Demonstrate SQLi and IDOR |
| Remediation | Fix the vulnerabilities |
| CI/CD | Add security checks before merge |
| Deployment | Remove debug mode/secrets |
| Maintenance | Continue scanning and patching |

## Important

This project is designed for a controlled local demonstration. Do not use the intentionally vulnerable version as a production application.
