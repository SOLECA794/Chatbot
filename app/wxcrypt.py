"""
WXBizMsgCrypt implementation (AES-CBC, PKCS7) adapted for WeCom/Tencent
"""
import base64
import struct
import time
from Crypto.Cipher import AES
import os

class WXBizMsgCrypt:
    def __init__(self, token, encoding_aes_key, corp_id):
        self.token = token
        self.corp_id = corp_id
        self.key = base64.b64decode(encoding_aes_key + "=")  # key is 43 chars base64 without =

    def _unpad(self, s):
        pad = s[-1]
        if pad < 1 or pad > 32:
            pad = 0
        return s[:-pad]

    def _pkcs7_pad(self, text):
        bs = AES.block_size
        padding = bs - len(text) % bs
        return text + bytes([padding]) * padding

    def encrypt(self, text):
        # Not needed for callback decrypt, placeholder
        raise NotImplementedError

    def decrypt(self, msg_signature, timestamp, nonce, post_data):
        # post_data is the raw XML string containing <Encrypt>...</Encrypt> or raw base64 cipher
        # Try to extract base64 payload
        import re
        m = re.search(r'<Encrypt>([^<]+)</Encrypt>', post_data)
        if m:
            encrypted = m.group(1)
        else:
            encrypted = post_data.decode() if isinstance(post_data, bytes) else str(post_data)
        try:
            cipher_text = base64.b64decode(encrypted)
        except Exception as e:
            return 40001, None
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.key[:16])
            decrypted = cipher.decrypt(cipher_text)
            decrypted = self._unpad(decrypted)
            # remove 16 random bytes, 4 bytes msg_len, then msg, then corpId
            content = decrypted[16:]
            msg_len = struct.unpack('!I', content[:4])[0]
            msg = content[4:4+msg_len].decode('utf-8')
            from_corp_id = content[4+msg_len:].decode('utf-8')
            if from_corp_id != self.corp_id:
                return 40005, None
            return 0, msg
        except Exception as e:
            return 40006, None

    def verify_url(self, msg_signature, timestamp, nonce, echostr):
        # echostr is base64 encoded encrypted random string
        try:
            cipher_text = base64.b64decode(echostr)
        except Exception:
            return 40002, None
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.key[:16])
            decrypted = cipher.decrypt(cipher_text)
            decrypted = self._unpad(decrypted)
            # first 16 random, then 4 bytes msg_len, then msg, then corpId
            content = decrypted[16:]
            msg_len = struct.unpack('!I', content[:4])[0]
            msg = content[4:4+msg_len].decode('utf-8')
            from_corp_id = content[4+msg_len:].decode('utf-8')
            if from_corp_id != self.corp_id:
                return 40005, None
            return 0, msg
        except Exception:
            return 40006, None
