# Chapter 5: Top API configuration and management vulnerabilities

This chapter continues the analysis of the OWASP top 10 security threats for APIs and offers a detailed 
break down of the following vulnerabilities:

- Unrestricted resource consumption
- Server-side request forgery (SSRF)
- Security misconfiguration
- Improper inventory management
- Unsafe consumption of APIs

Every vulnerability is explained in an accessible language with plenty of real-world examples and practical 
coding illustrations.

## Setting up the environment

To run the code examples for this chapter, clone the repo, `cd` into this folder, and install the 
dependencies using uv:

`uv sync`

Then activate the environment:

`source .venv/bin/activate`

Now you are ready to run the code examples.

## Running the code examples

Every vulnerability is illustrated in a dedicated file, which contains two versions of the same API:
- The vulnerable version
- The non-vulnerable version

Here's a walk through:

### Unrestricted resource consumption

Unrestricted resource consumption is illustrated in bola.py. To run the example, use the following command:

```uvicorn unrestricted resource consumption:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 1 endpoint:

* GET `/login`

In this case, the API is Unrestricted resource consumption when the `prevent_brute_force_login()` 
middleware isn't enabled. To disable it, comment out the line 21 of the code and run the server. 
To re-enable the middleware, uncomment the line.

### SSRF

SSRF is illustrated in broken_authentication.py. To run the example, use the following command:

```uvicorn ssrf:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 2 endpoints:

* GET `/vulnerable/ssrf`, which is vulnerable to SSRF
* GET `/ssrf`, which is not vulnerable to SSRF

### Security misconfiguration

Security misconfiguration is illustrated in security_misconfiguration.py. To run the example, use the following command:

```uvicorn security_misconfiguration:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 1 endpoint:

* GET `/users`

In this case, the API is vulnerable when the serve runs in debug mode. Debug mode is enabled in line 44.
To disable debug mode, turn the `debug` flag to `False`.

### Unsafe consumption of APIs

Unsafe consumption of APIs is illustrated in unsafe_consumption_apis.py. To run the example, use the following command:

```uvicorn unsafe_consumption_apis:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 4 endpoints:

* GET `/server-a/unsafe-api`, which is the compromised third-party API
* GET `/server-b/unsafe-consumption`, which is vulnerable to unsafe consumption of APIs
* GET `/server-b/safe-consumption`, which is not vulnerable to unsafe consumption of APIs
* GET `/server-b/characters`, which allows you to get a list of the characters
