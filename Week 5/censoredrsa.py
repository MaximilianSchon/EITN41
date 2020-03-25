from pyasn1.codec.der.decoder import decode
from pyasn1.codec.der.encoder import encode
from pyasn1_modules import rfc8017
from Cryptodome.PublicKey import RSA
import base64

encrypted = "Oz6BDHz59lqZeaOWxQypAEf9dC0S2ldMgqJt9ejm4WOEHVeAeDfM8m54OWYzwLKiY8JI1WO0FWMGfKQkESKeQoYvGc+Hhwyy2VBwa/AcSYICBySycu2qgzODXvXdzBnodRsA12kInC10v5ns1RY2SaEQ+t1yvzTXPKij8GU1K+g="

with open("key.pem", 'r') as file:
    key = ''.join(file.readlines()[1:-1])
    binarykey = base64.b64decode(key)
    decoded, rest = decode(binarykey, asn1spec=rfc8017)
    decoded[1] = decoded[4]*decoded[5]
    encoded = encode(decoded)
    key = encoded
    keyPriv = RSA.import_key(key)
    private_key = RSA.construct((keyPriv.n, keyPriv.e, keyPriv.d, keyPriv.p, keyPriv.q))
    decrypted_int = pow(int.from_bytes(base64.b64decode(encrypted), 'big'), keyPriv.d, keyPriv.n)
    decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
    print(decrypted_bytes)