import hashlib
from Crypto import Random
import base64
from base64 import b64encode, b64decode
from Crypto.Hash import MD5
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

RSA_PUBLIC = """MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC727VsVmN
                TXwzYCnqm1vQrD/cDQBqQd7PB2Ccapn9u3rR0HwDDYDgPK5
                oIk2/fhxigVGTXDozKUypK9mxBI9Cdo6l1PG6BluJ1FGU2j
                NeG+Fqa5eYV+dsa28+nJbNRlIR/aVQVzAQP+EQ6r8RSkB5iL
                Zr+4xyvdIFnUsrQWaGJ6QIDAQAB"""

RSA_PRIVATE = """MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBALvbtWxWY1NfDNgK
eqbW9CsP9wNAGpB3s8HYJxqmf27etHQfAMNgOA8rmgiTb9+HGKBUZNcOjMpTKkr2
bEEj0J2jqXU8boGW4nUUZTaM14b4Wprl5hX52xrbz6cls1GUhH9pVBXMBA/4RDqv
xFKQHmItmv7jHK90gWdSytBZoYnpAgMBAAECgYAwO9JSNcAc+Ou4UMB7M/fPUrMO
j5gCfemWnOQ1cIiJs/7LTeaJQ5xBMOXEy+5Oi0ZkbCbUHPVDQaU7SBg1hXebgXgg
jDpyCT3PlrX+F0pUvt5IBNwHRainMvWR6AMKfhJ7pIaQPdXEe9V4aDBwk9UFAkDe
F3hSEsjOLWmImy1tbQJBANfE5KOcrhP2AjlwM93GlBSkVWD8zsgQX5jdqGMoSJ5V
eZgkBYhlG7dmwfAABuYiAXtf5vnX0n3l7BnPpqib88sCQQDe4pJTbihY85Ygt88a
9HfiV6T3qsNjY7jZMuImQQ7/753Y0mWLt96E5rfIzlcR8mKAouApzIudRlDhM+jT
LQqbAkBoKnbTAfYMTuzd++weOhsNKBTL4OCXN0hfjUsYq777KXqtV16QbXeHAAXK
rsil227pt+/TWD0XaKOmBliH99onAkEA1z1kY694xVYOv+/h0D0P3QQYqpg88ilm
ZFIQNTMUwjJrc+zS5ZeeCygniYNCcHFrkKA57AO9PBegmaqgh/bySwJBANR4c2X4
v/zYf13fT+ivH5oD1tycXuzLw/UDtK3NoilocjLX+k2Sr27Jwd6tVotM98oX1MPt
vPvy3KGjqq/VrD0="""

random_generator = Random.new().read

class RsaHelper:

    @staticmethod
    def rsa_encrypt(msg):
        pubkey_str = """-----BEGIN PUBLIC KEY-----""" + '\n' + \
            RSA_PRIVATE + '\n' + """-----END PUBLIC KEY-----"""
        msg = msg.encode(encoding="utf-8")
        length = len(msg)
        default_length = 117
        # 公鑰加密
        pubobj = Cipher_pkcs1_v1_5.new(RSA.importKey(pubkey_str))
        # 長度不用分段
        if length < default_length:
            # print('加密不分段')
            encry_text = base64.b64encode(pubobj.encrypt(msg))
            encry_value = encry_text.decode('utf8')
            return encry_value
        # 需要分段
        offset = 0
        res = []
        encrypt_byte = ''

        while length - offset > 0:
            # print('加密要分段')
            if length - offset > default_length:
                encrypt_msg = pubobj.encrypt(
                    msg[offset:offset + default_length])
                # print('encrypt_msg')
                # print(encrypt_msg)
                # print(len(encrypt_msg))

                base64_msg = base64.b64encode(encrypt_msg)
                # print('base64_msg')
                # print(base64_msg)
                # print(len(base64_msg))
                res.append(base64_msg.decode("utf-8"))
                # res.append(encrypt_msg)

            else:
                encrypt_msg = pubobj.encrypt(msg[offset:])
                # print('encrypt_msg')
                # print(encrypt_msg)
                # print(len(encrypt_msg))

                base64_msg = base64.b64encode(encrypt_msg)
                # print('base64_msg')
                # print(base64_msg)
                # print(len(base64_msg))
                res.append(base64_msg.decode("utf-8"))

            offset += default_length
        return "".join(res)

    @staticmethod
    def rsa_decrypt(msg_str):
        # print('res_encrypt: ' + msg_str)
        prikey_str = """-----BEGIN RSA PRIVATE KEY-----""" + '\n' + \
            RSA_PRIVATE + '\n' + """-----END RSA PRIVATE KEY-----"""
        # msg_str = msg_str.encode('utf-8')
        length = len(msg_str)
        # print(length)
        default_length = 256
        # 長度不用分段
        if length <= default_length:
            # print('解密不用分段')
            rsakey = RSA.importKey(prikey_str)
            cipher = Cipher_pkcs1_v1_5.new(rsakey)
            text = cipher.decrypt(base64.b64decode(msg_str), random_generator)
            return str(text, encoding='utf-8')
        else:
            # 需要分段
            # print('解密要分段')
            default_length = 128
            priobj = Cipher_pkcs1_v1_5.new(RSA.importKey(prikey_str))
            msg_base64 = base64.b64decode(msg_str.encode('utf-8'))
            len_content = len(msg_base64)
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_length:
                    params_lst.append(priobj.decrypt(
                        msg_base64[offset: offset+default_length], prikey_str).decode('utf-8'))
                else:
                    params_lst.append(priobj.decrypt(
                        msg_base64[offset:], prikey_str).decode('utf-8'))
                offset += default_length
            return "".join(str(x) for x in params_lst)