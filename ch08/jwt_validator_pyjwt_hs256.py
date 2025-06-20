import jwt


def validate_token(token):
    return jwt.decode(
        jwt=token,
        key="password",
        algorithms=["HS256"],
        audience="https://apithreats.com/api",
        issuer="https://auth.apithreats.com",
    )


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguYXBpdGhyZWF0cy5jb20iLCJzdWIiOiIyMzQ1NjU0MyIsImF1ZCI6Imh0dHBzOi8vYXBpdGhyZWF0cy5jb20vYXBpIiwiaWF0IjoxNzMxNjYzMzE3LCJleHAiOjE3MzE2NjY5MTcuOTY0ODMxfQ.Jc3WamRnXTE8jse0w_6xG7jRH__6KF3LujN3hbEzmgE"
print(validate_token(token))
