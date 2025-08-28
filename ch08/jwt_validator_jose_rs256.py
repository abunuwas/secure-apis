from pathlib import Path

from jose import jwt

public_certificate = Path("public_key.pem").read_text()


def validate_token(token):
    return jwt.decode(
        token,
        key=public_certificate,
        audience="https://apithreats.com/api",
        issuer="https://auth.apithreats.com",
        algorithms="RS256",
    )


token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguYXBpdGhyZWF0cy5jb20iLCJzdWIiOiIyMzQ1NjU0MyIsImF1ZCI6Imh0dHBzOi8vYXBpdGhyZWF0cy5jb20vYXBpIiwiaWF0IjoxNzU2MzU3MDg2LCJleHAiOjE3NTYzNjA2ODZ9.pSAKr0mb5YcBzfBJvJ8H06ABqvDPr3eRRyPsw6iW9CmfLpFOFuxib6mjfvyEqoWQ0V7DBbtTCk5dwO3NSgA7JojN6edgctt2PvlY9Bf5SvOIC0aVYsYPvDhVH6ZEsFpGvVxgNO2IfO5CEzpG1fvxQCFyF7h_th7Pe_UlCWT1avCu_cANr3xiU8Iuq8mDVfdKpZ-Q18EopjiseuJvTaPSguJVNGBF42ryUoTW2ZP-3ns9Gvk1_nwWlvph6Ahl1GMmTwBA1-tg2GVjsp5kW-hRmxtQLdqGmw1cSjRp-mqkTBCsWFkSo0Gs82H1bKBL95i7Rjo7E9UGsv5outU3SUZBLXQVSXA67bvzixqKD3lsruxQUrAFjfugiLpO4bWqsxISDEg5GNZCMVMJCLV-TuhH5ua22NFAgXl0l8nrfLFmM-iD-q_tUH2SRcXRQy4oKuIW-WFkGxom_204YCNwmiDWilZQwHDZP3xk_jXRW83d5xoC9uieAKkk7ZvUoE7X8l3d"
print(validate_token(token))
