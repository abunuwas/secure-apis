from pathlib import Path

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_public_key

public_key = load_pem_public_key(Path("public_key.pem").read_text().encode())


def validate_token(token):
    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=["PS256"],
        audience="https://apithreats.com/api",
        issuer="https://auth.apithreats.com",
    )


token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguYXBpdGhyZWF0cy5jb20iLCJzdWIiOiIyMzQ1NjU0MyIsImF1ZCI6Imh0dHBzOi8vYXBpdGhyZWF0cy5jb20vYXBpIiwiaWF0IjoxNzMxNjgxOTUyLCJleHAiOjE3MzE2ODU1NTIuNzk5Mzc2fQ.tn5T-F3qZbTdW5sdjyko8zYQQUcx1iLU0-Iis7MWEe2r2aYFgJ5wvGEPBFN_FzENO-GeHQ5FXw2fIJ6DW5qEczzu2f3lyHWQOBhJVVCg5VHvPqstBwnlfxUV8MpXQhZYTAaYR3tPmP3GUYlQJhF_1yqvYlgzT9JVBG7Bl8MHHzXJCfJL9VjHCo631GvWmAfahRX6k2J3iEAdcPM2uZXniH-kntEtp-7MHbgwMUUf8cL6tYGnmkv0UxVdLarOBMvV-10trrIdNSrGTBVBsePjyB1lI8UiDam-Ri4R826Nbb51EZvE4k-60bWEPHPrl2Q2bDN_b1ACZeBlT9O3Un6G7FywwcyqzBI4pxrvzHXqzIPOkug7cts99mcloLDR5CL6uBjT99PNuUACDuaLtdun77V1XwrNBgklMxuE51WtP3oscEI5MeS5ucfiKLO3W8_9YmlwOwtEQN6NWuUICkvLA6Ga7plUEgHbApFpjIsL2EngTX490bwQeJfkCgoa6q8p"
print(validate_token(token))
