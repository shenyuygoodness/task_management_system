# 20–25 Minute Live Demo Script

## 1. Start with the requirements

Say:

"We are building a simple task-management application. Users register, log in, and manage their own tasks."

Then add the security requirements:

- Users must only access their own tasks.
- Passwords must be securely stored.
- User input must never become executable SQL.
- Secrets must not be hardcoded.
- Security checks must happen before merge and deployment.

This demonstrates that security starts before code.

## 2. Threat model

Draw:

Browser -> Flask API -> Database

Ask:

- Can someone pretend to be another user? (Spoofing)
- Can someone change another user's task? (Tampering)
- Can someone read another user's task? (Information Disclosure)
- Can someone access functionality they should not? (Elevation of Privilege)
- Can someone overwhelm login? (Denial of Service)

Highlight IDOR as an authorization threat.

## 3. Build/dependency decision

Show `requirements.txt`.

Explain:

"Before we build, we should know what components we are bringing into the application and whether known vulnerabilities exist."

Use dependency/security scanning as the example.

## 4. AI-assisted development

Show two prompts.

Weak:

"Build me a Flask task management app with login and tasks."

Security-aware:

"Build a Flask task management app. Before generating code, identify security requirements, apply STRIDE to the main data flows, use parameterized queries, securely hash passwords, enforce server-side authorization for every task access, keep secrets out of source code, and explain the security decisions."

Ask:

"Which prompt gives us a better starting point?"

Then remind the audience:

"AI is an assistant, not a security approval."

## 5. Show the vulnerable code

Point at the SQL query.

Explain the danger without spending too long on the payload.

Then show the hardcoded secret and plaintext password storage.

## 6. Run Semgrep/SonarQube

Run the scanners.

The message:

"We are moving security into development instead of waiting for production."

## 7. Test like an attacker

Create Alice and Bob.

Alice creates task 1.

Bob attempts to access:

`/tasks/1`

Explain:

"Authentication tells us Bob is logged in. Authorization should decide whether Bob is allowed to access Alice's task."

This is the key teaching moment.

## 8. Fix

Change the authorization query to include the current user's ID.

Replace the SQL construction with parameterized SQL.

Replace plaintext passwords with password hashing.

Move the secret to an environment variable.

Disable debug mode.

## 9. Re-test

Run the same checks.

The expected result:

- Bob can no longer access Alice's task.
- SQL input is treated as data rather than SQL.
- Secrets are no longer stored in source.
- Automated security checks are part of the workflow.

## Closing line

"The goal of Shift Left is not to find every vulnerability before production. The goal is to make security part of the decisions we make while creating the software."
