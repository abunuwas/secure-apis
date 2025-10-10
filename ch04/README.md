# Chapter 4: Top API authentication and authorization vulnerabilities

This chapter introduces the OWASP top 10 security threats for APIs and offers a detailed break down of 
the following vulnerabilities:

- Broken object-level authorization (BOLA)
- Broken authentication
- Broken object property-level authorization (BOPLA)
- Broken function-level authorization (BFLA)
- Unrestricted access to sensitive business flows

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

### BOLA

BOLA is illustrated in bola.py. To run the example, use the following command:

```uvicorn bola:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 2 endpoints:

* GET `/vulnerable/orders/{order_id}`, which is vulnerable to BOLA
* GET `/orders/{order_id}`, which is not vulnerable to BOLA

### Broken authentication

Broken authentication is illustrated in broken_authentication.py. To run the example, use the following command:

```uvicorn broken_authentication:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 2 endpoints:

* GET `/vulnerable/validate-token`, which is vulnerable to broken authentication
* GET `/validate-token`, which is not vulnerable to broken authentication

To run the test here, you need to authenticate your requests.

First, obtain an access token by logging in with https://apithreats.com/login. Fetch the 
`access_token.token` property of the resulting payload.

Then, use that token to authorize your requests. To do that, go back to http://localhost:8000/docs and:

1. Click on the Authorize button on the to-right corner of the screen
2. In the modal, paste the access token from apithreats.com and click Authorize

You're ready to test the API.

### Broken object property-level authorization

#### Mass assignment

Mass assignment is illustrated in mass_assignment.py. To run the example, use the following command:

```uvicorn mass_assignment:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 2 endpoints:

* GET `/vulnerable/payments`, which is vulnerable to mass assignment
* GET `/payments/`, which is not vulnerable to mass assignment

#### Excessive data exposure

BOLA is illustrated in bola.py. To run the example, use the following command:

```uvicorn excessive_data_exposure:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 3 endpoints:

* POST `/set-me-up`, which allows you to configure your user as working for a certain project
* GET `/vulnerable/query-user`, which is vulnerable to excessive data exposure
* GET `/query-user`, which is not vulnerable to excessive data exposure

To test the API, you need to:
1. Obtain an access token and authorize your requests. Follow the steps in the Broken Authentication section for this
2. Use the POST `/set-me-up` endpoint to add your personal details and the project you're working on

With this, you're ready to test the API. For example, search for the user whose email is sara@apithreats.com.

### BFLA

BFLA is illustrated in bfla.py. To run the example, use the following command:

```uvicorn bfla:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 2 endpoints:

* GET `/vulnerable/admin`, which is vulnerable to bfla
* GET `/admin/`, which is not vulnerable to bfla

To test the API, you need to obtain an access token and authorize your requests. Follow the steps in 
Broken Authentication for this.

### Unrestricted access to sensitive business flows

Unrestricted access to sensitive business flows is illustrated in bfla.py. To run the example, use the following command:

```uvicorn vulnerable_business_flows:server --reload```

Visit https://localhost:8000/docs to load the Swagger UI for this API.

It contains 2 endpoints:

* GET `/tickets`
* GET `/checkout/`

In this case, the API is vulnerable to unrestricted access to sensitive business flows when the 
`prevent_scalping()` middleware isn't enabled. To disable it, comment out the line 58 of the code and 
run the server. To re-enable the middleware, uncomment the line.
