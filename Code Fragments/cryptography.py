"""
Some examples for how to use cryptography using the PyCrytodome module
 http://pycryptodome.readthedocs.io/en/latest/
 https://github.com/Legrandin/pycryptodome/tree/master/lib/Crypto/Cipher
 https://pypi.org/project/pycryptodomex/
install using:
pip install pycryptodomex
"""

#generate keys
# http://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html
from Cryptodome.PublicKey import ECC
key = ECC.generate(curve='P-256')
privateKey = key.export_key(format='DER', compress=True)
print("PrivateKey:\n" + str(privateKey.hex()))
print("Length: " + str(len(privateKey)))
publicKey1 = key.public_key().export_key(format='DER', compress=True)
print("PublicKey Compressed:\n" + str(publicKey1.hex()))
print("Length: " + str(len(publicKey1)))
publicKey2 = key.public_key().export_key(format='DER', compress=False)
print("PublicKey:\n" + str(publicKey2.hex()))
print("Length: " + str(len(publicKey2)))


#sign a message
# http://pycryptodome.readthedocs.io/en/latest/src/signature/dsa.html
from Cryptodome.Hash import SHA256 #can use SHA512 (and others) as well
from Cryptodome.Signature import DSS
message = "This is a test".ljust(256,"_")
h1 = SHA256.new(message.encode())
print("Message hash generator: " + str(h1))

signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(h1)
print("Signiture:\n" + str(signature.hex()))
print("Length: " + str(len(signature)))

'''
test = bytearray(len(publicKey1))
for i in range(0,len(publicKey1)):
    if i != 56:
        test[i] = publicKey1[i]
    else:
        test[i] = 0
test = bytes(test)
print(test.hex())
'''

#verify signature
received_message = message.encode()
received_key = ECC.import_key(publicKey1)
h2 = SHA256.new(received_message)
#verifier = DSS.new(key.public_key(), 'fips-186-3')
verifier = DSS.new(received_key, 'fips-186-3')
try:
    verifier.verify(h2, signature)
    print("The message is authentic.")
except ValueError:
    print("The message is not authentic.")

#encrypt and decrypt data
#Encryption via ECC is not supported (yet I hope)
# https://github.com/Legrandin/pycryptodome/issues/139


