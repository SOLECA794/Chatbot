from fastapi import FastAPI, Request, HTTPException
import os
import logging
import xml.etree.ElementTree as ET
from app.wxcrypt import WXBizMsgCrypt

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# load from env
CORP_ID = os.getenv('CORP_ID')
TOKEN = os.getenv('TOKEN')
ENCODING_AES_KEY = os.getenv('ENCODING_AES_KEY')

if not (CORP_ID and TOKEN and ENCODING_AES_KEY):
    logging.warning('CORP_ID/TOKEN/ENCODING_AES_KEY not fully configured in env. GET/POST will still run but verification may fail.')

wxcrypt = None
if CORP_ID and TOKEN and ENCODING_AES_KEY:
    try:
        wxcrypt = WXBizMsgCrypt(TOKEN, ENCODING_AES_KEY, CORP_ID)
    except Exception as e:
        logging.exception('failed init wxcrypt: %s', e)


@app.get('/callback')
async def verify(msg_signature: str = None, timestamp: str = None, nonce: str = None, echostr: str = None):
    """Handle the verification GET from WeCom. Return decrypted echostr as plain text when available."""
    logging.info('GET /callback called with signature=%s timestamp=%s nonce=%s echostr=%s', msg_signature, timestamp, nonce, echostr)
    if not wxcrypt:
        # fallback: return echostr raw
        return echostr or 'ok'
    if not (msg_signature and timestamp and nonce and echostr):
        raise HTTPException(status_code=400, detail='missing params')
    code, plaintext = wxcrypt.verify_url(msg_signature, timestamp, nonce, echostr)
    if code != 0:
        logging.error('verify_url failed code=%s', code)
        raise HTTPException(status_code=400, detail=f'verify failed: {code}')
    return plaintext


@app.post('/callback')
async def callback(request: Request):
    """Receive encrypted XML POST from WeCom, decrypt and log parsed message."""
    params = request.query_params
    msg_signature = params.get('msg_signature') or params.get('msg_signature')
    timestamp = params.get('timestamp')
    nonce = params.get('nonce')
    body = await request.body()
    logging.info('POST /callback received. sig=%s ts=%s nonce=%s body_len=%d', msg_signature, timestamp, nonce, len(body))

    if not wxcrypt:
        logging.warning('wxcrypt not configured; cannot decrypt. Returning success to avoid retry storms.')
        return 'success'

    code, plaintext = wxcrypt.decrypt(msg_signature, timestamp, nonce, body)
    if code != 0:
        logging.error('decrypt failed code=%s', code)
        # return success to avoid retries; but log error for debugging
        return 'success'

    logging.info('decrypted message: %s', plaintext)

    # parse plaintext XML
    try:
        xml_root = ET.fromstring(plaintext)
        msg_type = xml_root.findtext('MsgType')
        from_user = xml_root.findtext('FromUserName')
        to_user = xml_root.findtext('ToUserName')
        content = xml_root.findtext('Content') or ''
        is_at = xml_root.findtext('IsAt') or '0'

        logging.info('parsed msg: type=%s from=%s to=%s is_at=%s content=%s', msg_type, from_user, to_user, is_at, content)

        # Simple auto-reply decision logic (no send implemented yet)
        wake_words = ['家帮', '家庭助理', '小助手']
        should_reply = False
        if is_at == '1':
            should_reply = True
        else:
            for w in wake_words:
                if w in content:
                    should_reply = True
                    break

        if should_reply:
            # For now just log that we'd reply; actual sending implemented in next task
            logging.info('Message qualifies for auto-reply (would send reply here).')
        else:
            logging.info('No reply triggered for this message.')

    except Exception as e:
        logging.exception('failed parse plaintext xml: %s', e)

    # Always return success to WeCom to avoid retries
    return 'success'
