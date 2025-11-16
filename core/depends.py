import os

from fastapi import Header, HTTPException, status

API_KEY = os.getenv("API_KEY", 'supersecretkey')


async def api_key_header(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
