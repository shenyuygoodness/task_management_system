# Secure Remediation Guide

This document is the second half of the live demonstration.

## SQL Injection

### Vulnerable

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
user = conn.execute(query).fetchone()
```

The user's input becomes part of the SQL statement.

### Secure

```python
user = conn.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
).fetchone()
```

Better still, passwords should not be compared directly. Store a password hash and verify it using a password-hashing library.

---

## IDOR / Broken Object Level Authorization

### Vulnerable

```python
task = conn.execute(
    "SELECT * FROM tasks WHERE id = ?",
    (task_id,)
).fetchone()
```

The application checks that the task exists, but not that it belongs to the current user.

### Secure

```python
task = conn.execute(
    "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
    (task_id, session["user_id"])
).fetchone()
```

The authorization decision must happen on the server.

---

## Hardcoded secret

### Vulnerable

```python
app.secret_key = "demo-secret-key"
```

### Secure

```python
app.secret_key = os.environ["FLASK_SECRET_KEY"]
```

The production secret should be supplied through an appropriate secret-management mechanism.

---

## Plaintext passwords

The demonstration version stores passwords directly in SQLite.

For a real application, use a password hashing function such as Werkzeug's password hashing helpers or another established password-hashing library.

The key lesson:

**Encryption is not the same thing as password hashing.**

---

## Debug mode

### Vulnerable

```python
app.run(debug=True)
```

### Secure

```python
app.run(debug=False)
```

Production deployments should use a proper production server and deployment configuration.

---

## Shift Left lesson

Notice that these fixes are not all "testing problems."

- The secret problem starts in implementation/configuration.
- The IDOR problem comes from an authorization/design decision.
- SQL injection comes from an unsafe coding pattern.
- Plaintext passwords come from an insecure authentication design.
- Debug mode becomes a deployment/configuration issue.

That is why security should run through the SDLC rather than being treated as a final testing phase.
