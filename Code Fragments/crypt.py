from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
public_key = private_key.public_key()

#serialized_private = private_key.private_bytes(
#    encoding=serialization.Encoding.PEM,
#    format=serialization.PrivateFormat.PKCS8,
#    encryption_algorithm=serialization.BestAvailableEncryption(b'testpassword')
#)

serialized_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

serialized_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

#serialized_private = private_key.private_bytes(
#    encoding=serialization.Encoding.PEM,
#    format=serialization.PublicFormat.OpenSSH
#)

import base64
print(serialized_public[26 + 1:-26])
print(len(base64.b64decode(serialized_public[26 + 1:-26])))
