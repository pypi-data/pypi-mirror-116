# -*- coding: utf-8 -*-

import base64
import json

# pip install  pycryptodome
from Crypto.Cipher import AES

# 128位分组
BLOCK_SIZE = AES.block_size


# 补位
def pad(s, length):
    return s + (BLOCK_SIZE - length % BLOCK_SIZE) * chr(BLOCK_SIZE - length % BLOCK_SIZE)


def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def encrypt_content(_content, _encrypt_type, _encrypt_key, _charset):
    if "AES" == _encrypt_type.upper():
        return aes_encrypt_content(_content, _encrypt_key, _charset)
    raise Exception("unsupported encrypt_type=" + _encrypt_type)


def aes_encrypt_content(_content, _encrypt_key, _charset):
    """
    使用AES算法进行对称加密
    :param _content:
    :param _encrypt_key:
    :param _charset:
    :return:
    """
    length = len(bytes(_content, encoding=_charset))
    padded_content = pad(_content, length)
    iv = b'\0' * BLOCK_SIZE
    # 创建加密方式
    cryptor = AES.new(_encrypt_key.encode(), AES.MODE_CBC, iv)
    # 加密
    _encrypted_content = cryptor.encrypt(padded_content.encode())
    # 将加密结果转换为b64encode编码字节
    _encrypted_content = base64.b64encode(_encrypted_content)
    # 将字节转换成字符串
    _encrypted_content = str(_encrypted_content, encoding=_charset)
    return _encrypted_content


def decrypt_content(_encrypted_content, _encrypt_type, _encrypt_key, _charset):
    if "AES" == _encrypt_type.upper():
        return aes_decrypt_content(_encrypted_content, _encrypt_key, _charset)
    raise Exception("当前不支持该算法类型encrypt_type=" + _encrypt_type)


def aes_decrypt_content(_encrypted_content, _encrypt_key, _charset):
    _encrypted_content = base64.b64decode(_encrypted_content)
    iv = b'\0' * BLOCK_SIZE
    cryptor = AES.new(_encrypt_key.encode(), AES.MODE_CBC, iv)
    _content = unpad(cryptor.decrypt(_encrypted_content))
    _content = _content.decode(_charset)
    return _content


def decode_data(data, sso_secret_key):
    data = base64.urlsafe_b64decode(data)
    data = decrypt_content(data, "AES", sso_secret_key, "utf-8")
    data = json.loads(data)
    return data


def encode_data(data, sso_secret_key):
    data = json.dumps(data)
    data = encrypt_content(data, "AES", sso_secret_key, "utf-8")
    data = base64.urlsafe_b64encode(data.encode()).decode()
    return data


if __name__ == "__main__":
    encrypt_type = "aes"
    encrypt_key = "1234567891234567"
    content = "hello world"
    charset = "utf-8"
    encrypted_content = encrypt_content(content, encrypt_type, encrypt_key, charset)
    print(encrypted_content)
    res = decrypt_content(encrypted_content, encrypt_type, encrypt_key, charset)
    print(res)
