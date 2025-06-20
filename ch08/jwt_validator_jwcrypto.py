import base64
import json
from datetime import datetime, timezone
from pathlib import Path

from jwcrypto import jwk, jwt

public_certificate = Path("public_key.pem").read_text()
jwk_key = jwk.JWK()
jwk_key.import_from_pem(data=public_certificate.encode())


def validate_token(token):
    unverified_header = json.loads(base64.urlsafe_b64decode(token.split(".")[0]))
    encrypted_token = jwt.JWT(
        key=jwk_key,
        jwt=token,
        algs=[unverified_header["alg"]],
        check_claims={
            "aud": "https://pyjobs.works/jobs",
            "exp": datetime.now(timezone.utc).timestamp(),
        },
    )
    return encrypted_token.claims


token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgucHlqb2JzLndvcmtzIiwic3ViIjoiMjM0NTY1NDMiLCJhdWQiOiJodHRwczovL3B5am9icy53b3Jrcy9qb2JzIiwiaWF0IjoxNjYyOTc1OTE1Ljk0NTk1NSwiZXhwIjoxNjYyOTc5NTE1Ljk0NTk1NX0.Ir-YMQSlcB5QdWzmRgmEd686MAQtuQYlY9loM7FxCguRjbJ4PJiLGS8zEK8UfRbv9UWsASe8vjt30nUt4eJaoN9nQ7yCrjZRnuOaCvE0dLyK0ogpnR7gKSQxCEOgQFD8fUwOE9xog9SALOKWaoWtgZhm2RKZBDcD0-XUBIzg2sJs6viR4zjj1OISKalMN2qc-VUFFRkvQy6DcPaw4qjGQSgUr6Nyh59R1iEI7_JM6tWAJLuB7y4fKl6n0MOpOiLJrgbIhx0piqu0b6zqvES3cHDfvWLt8swaxtXM54muQLw7gO-dQztysKBufNs1NYf-h-osM561FdGTtehnQIOxvw"
print(validate_token(token))
