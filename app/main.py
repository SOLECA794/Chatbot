from fastapi import FastAPI, Request, HTTPException
import os
from wechatpy.exceptions import InvalidSignature

app = FastAPI()

@app.get("/callback")
async def verify(msg_signature: str = None, timestamp: str = None, nonce: str = None, echostr: str = None):
    # 验证回调 URL 的处理（占位）
    return echostr or "ok"

@app.post("/callback")
async def callback(request: Request):
    # 解密并处理消息（占位）
    payload = await request.body()
    return "success"
