from jose import jwt


def validate_token(token):
    return jwt.decode(
        token, key="password", audience="https://pyconus2024.com", algorithms="HS256"
    )


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguYXBpdGhyZWF0cy5jb20iLCJzdWIiOiIxMCIsImF1ZCI6Imh0dHBzOi8vcHljb251czIwMjQuY29tIiwiaWF0IjoxNzE1ODg4MjAxLjY0NjA5MywiZXhwIjoxNzE1ODkxODAxLjY0NjA5M30.vho8eG1gkPSoXg4HnE3QqUV2DD-yTPRXV3ZGFTJfbNQ"
print(validate_token(token))
