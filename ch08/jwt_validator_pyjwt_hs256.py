import jwt


def validate_token(token):
    return jwt.decode(
        jwt=token,
        key="password",
        algorithms=["HS256"],
        audience="https://apithreats.com/api",
        issuer="https://auth.apithreats.com",
    )


token = "<token>"  # paste your token here
print(validate_token(token))
