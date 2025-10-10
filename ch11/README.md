# Chapter 8: Implementing API authentication and authorization

This chapter teaches you how to leverage observability for API security using the OpenTelemetry standard.

## Setting up the environment

To run the code examples for this chapter, clone the repo, `cd` into this folder, and install the 
dependencies using uv:

`uv sync`

Then activate the environment:

`source .venv/bin/activate`

Follow the additional steps outlined in the chapter to bootstrap your dependencies for OTel.

Now you are ready to run the code examples.

## Testing the API

To test the API, first run the server using the following command:

```opentelemetry-instrument --traces_exporter console --metrics_exporter console --logs_exporter console uvicorn server:server```

Then visit http://localhost:8000/docs to load the Swagger UI for the API.

To call authenticated endpoints, you need to obtain an access token, which you can obtain by calling the 
* POST /login endpoint through the Swagger UI. Provide any value of your choice for the body parameters and you'll get an access token back.

Then, use that token to authorize your requests. To do that, go back to http://localhost:8000/docs and:

1. Click on the Authorize button on the to-right corner of the screen
2. In the modal, paste the access token from apithreats.com and click Authorize

You're ready to start testing the API.
