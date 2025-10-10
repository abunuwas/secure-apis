# Chapter 8: Implementing API authentication and authorization

This chapter walks you through the steps needed to implement robust authentication and authorization for 
your APIs using an OIDC provider.

## Setting up the environment

To run the code examples for this chapter, clone the repo, `cd` into this folder, and install the 
dependencies using uv:

`uv sync`

Then activate the environment:

`source .venv/bin/activate`

Now you are ready to run the code examples.

## Running the JWT code examples

In this folder, you'll find examples of generating and validating JWTs using Python's most popular JWT 
libraries. I've included examples using HS256, RS256, and PS256 signatures when possible if supported by 
the library.

## Running the API server

To run the API server, you need some configuration first. Follow the steps in chapter 8 and Appendix B
where needed to set up a tenant in Auth0 (free tier). Then, populate the required configuration values 
in the `.env` file. Below are the configruations you'll need:

* AUTH0_CLIENT_ID: your Auth0 client ID
* AUTH0_CLIENT_SECRET: your Auth0 client secret
* AUTH0_ADMIN_CLIENT_ID: your Auth0 admin client ID
* AUTH0_ADMIN_CLIENT_SECRET: your Auth0 admin client secret
* JWKS_ENDPOINT: your JWKS endpoint

**DO NOT** push this configuration to GitHub. Keep these values in hour local file system only.

Once you have the config ready, export the values to the environment using the following command:

```. ./.env```

Then run the server:

```uvicorn api:server --reload```
