import random

'''attempt to make a kademilaID using the cryptokey concatonated with the count of the number of binary '1's in the key (the 'routing' byte)
This method will no work as the 'routing' byte gets a bell curve distribution, instead of required normal distribution
'''
print("Start ID test1")
cryptoID = random.randint(0, 2**512 - 1) #a stand in for a crytographic key
count = 0
temp = cryptoID
for i in range(0, 512):
    if temp % 2 == 1:
        count += 1
    temp = temp>>1
kademilaID = ((count // 2) * 2**512) + cryptoID
print("\t", cryptoID)
print("\t", count)
print("\t", kademilaID)

'''this method will take the cryptokey, and copy the last (least significant) byte for the 'routing' byte'''
print("Start ID test2")
cryptoID = random.randint(0, 2**512 - 1) #a stand in for a crytographic key
routingByte = cryptoID % 256
kademilaID = routingByte * 2**512 + cryptoID
print("\t", cryptoID)
print("\t", routingByte)
print("\t", kademilaID)

'''attempt at generating and managing a public/private key setup
NOTE: this uses the 'Cryptohtaphy' module
install is using '$ pip install cryptography'
'''
'''
print("cryptography examples")
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/
# https://arstechnica.com/security/2013/10/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/ #an explination of how elliptic curve cryptography works

#Elliptic Curve Signature Algorithms
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
private_key = ec.generate_private_key(
    ec.SECP384R1(), default_backend()
)
data = b"this is some data I'd like to sign"
signature = private_key.sign(
    data,
    ec.ECDSA(hashes.SHA256())
)

# If your data is too large to be passed in a single call, you can hash it separately and pass that value using Prehashed
from cryptography.hazmat.primitives.asymmetric import utils
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash, default_backend())
hasher.update(b"data & ")
hasher.update(b"more data")
digest = hasher.finalize()
sig = private_key.sign(
    digest,
    ec.ECDSA(utils.Prehashed(chosen_hash))
)

# Verification requires the public key, the signature itself, the signed data, and knowledge of the hashing algorithm that was used when producing the signature
public_key = private_key.public_key()
public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))

# If your data is too large to be passed in a single call, you can hash it separately and pass that value using Prehashed
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash, default_backend())
hasher.update(b"data & ")
hasher.update(b"more data")
digest = hasher.finalize()
public_key.verify(
    sig,
    digest,
    ec.ECDSA(utils.Prehashed(chosen_hash))
)

# Serializing the keys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
serialized_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'testpassword')
)
serialized_private.splitlines()[0]

public_key = private_key.public_key()
serialized_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
serialized_public.splitlines()[0]

public = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)
'''
'''welp, the above was a nightmare to understand, many different classes and references to different things, my head is spinning'''

'''This uses a pure python ECC implimentation
# https://github.com/amintos/PyECC
'''
print("PyECC stuff")
import ecc.Key
import math
for i in range(0,16):
    testkey = ecc.Key.Key.generate(256)
    print(testkey)
    print(testkey.encode())
    print(len(testkey.encode()))
    print(len(testkey.encode(True)))
    print(testkey._priv[1])
    print(math.log2(testkey._priv[1]))
    print(testkey._pub[1])
    print(testkey._pub[1][0])
    print(math.log2(testkey._pub[1][0]))
    print(testkey._pub[1][1])
    print(math.log2(testkey._pub[1][1]))
    
