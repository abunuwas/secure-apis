from pathlib import Path

from jose import jwt

public_certificate = Path("public_key.pem").read_text()


def validate_token(token):
    return jwt.decode(
        token,
        key=public_certificate,
        audience="https://pyjobs.works/jobs",
        algorithms="RS256",
    )


token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgucHlqb2JzLndvcmtzIiwic3ViIjoiMjM0NTY1NDMiLCJhdWQiOiJodHRwczovL3B5am9icy53b3Jrcy9qb2JzIiwiaWF0IjoxNjYzMjM5MDYwLjQ4MTc2OSwiZXhwIjoxNjYzMjQyNjYwLjQ4MTc2OX0.BZKUqTuBD8JnXaaAXC9xsySqgtXgoJ9ZYOzqZmg46CHIm01IjsHuMYktJUwjLh6_OrrHvZpLz66NUEwZq4dyk4OdtIc1sJOukFJ1a7eX30V7u8gC9KL5fAR_01YyfuuykFz-ZCjSEuqPXDU9Ssjaz3636Oux7k6n2bUjeqr-aQwfO2eJRDwMm0jTMHkdfJD3NC3JwCj9Oeq2dQscKGoVYAPuo65kDA2XhnlIoxqCCcsSWu9gLMhgxUCF8ZrgAQfXsnmltyukd4IcPVwP5PvGDpY48oPBYbxSvHGMOQu_ihxwZi6LS-OX3_fjTPScZ4EMXqmH23qA2Lz8RFxgxPcT2g"
print(validate_token(token))
