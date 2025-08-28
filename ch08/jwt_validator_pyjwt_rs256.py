from pathlib import Path

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# x509_certificate = load_pem_x509_certificate(
#     Path("public_key.pem").read_text().encode()
# ).public_key()

public_key = load_pem_public_key(Path("public_key.pem").read_text().encode())


def validate_token(token):
    return jwt.decode(
        token,
        key=public_key,
        algorithms="RS256",
        audience="https://apithreats.com/api",
        issuer="https://auth.apithreats.com",
    )


token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguYXBpdGhyZWF0cy5jb20iLCJzdWIiOiIyMzQ1NjU0MyIsImF1ZCI6Imh0dHBzOi8vYXBpdGhyZWF0cy5jb20vYXBpIiwiaWF0IjoxNzU2MzU3NTExLCJleHAiOjE3NTYzNjExMTF9.ZenH66bXR6lYyntGuy7-haQrRfgnq-gqVsEavOLTzlXZ6IAOH7JTe4fPF3_vuI9TCSALD5iOqe6qtO1bHF9l_qwAAvGOJy3NWetkCD5FeRDi5fAKJF6MpcfV1JO7QDSqRcWIKYcg-cEOjE7BJ_2Lao_rMJ3cRCT8Qv2qFn7s5qwsdGr3ikepuL4ljlCbOv-DYEAT2oVvbmilrCiBSIEWwlVEGatLdtTdpEbI_NPg3ns-eLN2BKH5BAyWSBUGuYnJsMbq_-gqsbFRI_YsWovfHTWMFj3yTgglNOimmP9R4qYq62aXpApmvco_MMDfi3YogUWX4qQZ_buFD6X_X6GtNdOneszrrBrTdVjJdi2Sb09zRCLDmwMgHUnPCCD3QOIF-G8jdGI0fQ7Vc7FGQWiLE5rIFwUgomRtMDsOPShzVa31H2WC6L4pu0hOKRW4Gn15PYPfLVd3tuSlDANWsFoRfY6IPYFY4FYB_SFum8cnPbz4QPJUR3RsVDEAPtHjiFJM"
print(validate_token(token))
