# FastAPI JWT Auth with httpOnly Cookies

## Problem

Implement JWT-based authentication in a FastAPI + React app where the token is stored
in an httpOnly cookie — not localStorage — so it is inaccessible to JavaScript and
protected from XSS attacks.

## Environment

- OS: Ubuntu
- Python: 3.11
- Stack: FastAPI + MySQL + React 18 + Axios

## Why This Works

`httpOnly` cookies are set by the server and never readable by `document.cookie` in
the browser. The browser automatically attaches them to every matching request.
This eliminates the entire class of XSS-based token theft that affects localStorage.

FastAPI reads the cookie via the `Cookie` dependency. The React frontend uses
`withCredentials: true` on all axios requests so the browser sends the cookie
cross-origin (when the backend allows it via CORS `allow_credentials=True`).

## Dependencies

```
# Backend
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1
fastapi==0.111.0

# Frontend
axios (npm)
```

## Backend Example

### services/auth.py
```python
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 24))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
```

### routes/auth.py — login sets cookie, logout clears it
```python
from fastapi import APIRouter, Response, Cookie, Depends, HTTPException
from jose import JWTError

router = APIRouter()
COOKIE_NAME = "access_token"

@router.post("/login")
def login(response: Response, credentials: LoginRequest, db=Depends(get_db)):
    user = get_user_by_username(db, credentials.username)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,       # JS cannot read this cookie
        samesite="lax",      # CSRF protection
        secure=False,        # Set True in production (HTTPS only)
        max_age=86400,       # 24 hours in seconds
    )
    return {"status": "success", "data": {"username": user.username}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=COOKIE_NAME)
    return {"status": "success", "data": None}

@router.get("/me")
def get_me(access_token: str = Cookie(None), db=Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = decode_token(access_token)
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {"status": "success", "data": {"username": user.username, "email": user.email}}
```

### main.py — CORS must allow credentials
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # explicit origin, not "*"
    allow_credentials=True,                   # required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Frontend Example

### services/api.js
```js
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,   // send cookies on every request
})

export const login = (data) => api.post('/login', data)
export const logout = () => api.post('/logout')
export const getMe = () => api.get('/me')
```

### DashboardPage.jsx — verify session on mount via /me
```jsx
useEffect(() => {
  getMe()
    .then(({ data }) => setUser(data.data))
    .catch(() => navigate('/login'))
}, [navigate])
```

## Notes

- **`allow_origins` must be explicit** when `allow_credentials=True` — `"*"` will cause a CORS error in the browser
- Set `secure=True` in production so the cookie is only sent over HTTPS
- `samesite="lax"` prevents the cookie being sent on cross-site POST requests (CSRF protection)
- No token is ever stored or read by JavaScript — the browser handles it transparently
- The `/me` endpoint is the canonical way to check auth state on page load
