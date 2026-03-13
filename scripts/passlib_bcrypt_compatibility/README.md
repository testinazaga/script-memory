# passlib + bcrypt Compatibility Fix

## Problem

FastAPI returns `500 Internal Server Error` on any endpoint that calls
`pwd_context.hash()` or `pwd_context.verify()`. Backend logs show:

```
File "/usr/local/lib/python3.11/site-packages/passlib/handlers/bcrypt.py", line 380, in detect_wrap_bug
    if verify(secret, bug_hash):
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary
```

## Environment

- OS: Ubuntu (Docker container, python:3.11-slim)
- Python: 3.11
- Stack: FastAPI + passlib 1.7.4

## Why This Happens

`passlib 1.7.4` runs a wrap-bug detection check when initializing the bcrypt backend.
This check calls `bcrypt.hashpw()` with a known test vector. In `bcrypt>=4.1`, the
library started enforcing a 72-byte password limit strictly and raises `ValueError`
instead of silently truncating — which breaks passlib's internal test and crashes the
entire `CryptContext` initialization.

`bcrypt==4.0.1` is the last version with behavior compatible with `passlib 1.7.4`.

## Fix

Pin `bcrypt==4.0.1` explicitly in `requirements.txt`:

```
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
```

Without the explicit pin, `pip` resolves `passlib[bcrypt]` to the latest bcrypt
(>=4.1) which breaks at runtime — not at install time.

## Verification

After rebuilding the container, test with:

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test1234"}'
# Expected: {"status": "success", "data": {"id": 1, ...}}
```

## Notes

- This is a known open issue: https://github.com/pypa/passlib/issues/684
- `passlib` is in maintenance mode — a full fix is unlikely upstream
- Alternative long-term fix: replace `passlib` with `bcrypt` directly:
  ```python
  import bcrypt
  def hash_password(password: str) -> str:
      return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  def verify_password(plain: str, hashed: str) -> bool:
      return bcrypt.checkpw(plain.encode(), hashed.encode())
  ```
- The pin `bcrypt==4.0.1` is safe — it supports all standard bcrypt operations
