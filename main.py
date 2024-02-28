import base64
import time

from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes


def password_encrypt(password):
    key_id = 41
    public_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvcu1KMDR1vzuBr9iYKW8\nKWmhT8CVUBRkchiO8861H7zIOYRwkQrkeHA+0mkBo3Ly1PiLXDkbKQZyeqZbspke\n4e7WgFNwT23jHfRMV/cNPxjPEy4kxNEbzLET6GlWepGdXFhzHfnS1PinGQzj0ZOU\nZM3pQjgGRL9fAf8brt1ewhQ5XtpvKFdPyQq5BkeFEDKoInDsC/yKDWRAx2twgPFr\nCYUzAB8/yXuL30ErTHT79bt3yTnv1fRtE19tROIlBuqruwSBk9gGq/LuvSECgsl5\nz4VcpHXhgZt6MhrAj6y9vAAxO2RVrt0Mq4OY4HgyYz9Wlr1vAxXXGAAYIvrhAYLP\n7QIDAQAB\n-----END PUBLIC KEY-----\n'
    session_key = get_random_bytes(32)
    iv = get_random_bytes(12)
    timestamp = str(int(time.time()))
    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_v1_5.new(recipient_key)
    rsa_encrypted = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
    cipher_aes.update(timestamp.encode())
    aes_encrypted, tag = cipher_aes.encrypt_and_digest(password.encode('utf8'))
    size_buffer = len(rsa_encrypted).to_bytes(2, byteorder='little')
    payload = base64.b64encode(b''.join([
        b'\x01',
        key_id.to_bytes(1, byteorder='big'),
        iv,
        size_buffer,
        rsa_encrypted,
        tag,
        aes_encrypted,
    ]))
    return f'#PWD_INSTAGRAM:1:{timestamp}:{payload.decode()}'


if __name__ == '__main__':
    print(password_encrypt('password'))
