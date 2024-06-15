import requests
from fastapi import FastAPI, HTTPException

server = FastAPI()


bad_domains = ["localhost", "127.0.0.1"]


@server.get("/secret", include_in_schema=False)
def secret():
    return "secret"


@server.get("/ssrf-vulnerable")
def ssrf_vulnerable(url: str):
    response = requests.get(url)
    return response.content


@server.get("/ssrf-mitigated")
def ssrf_mitigated(url: str):
    if any(domain in url for domain in bad_domains):
        raise HTTPException(status_code=422, detail=f"Forbidden domain in {url}")
    response = requests.get(url)
    return response.content
