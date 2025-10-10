# Chapter 12: Testing API security

This chapter teaches you how to test your APIs for design vulnerabilities, documentation drift, and check if 
your APIs are vulnerable to your threat models.

## Setting up the environment

To run the code examples for this chapter, clone the repo, `cd` into this folder, and install the 
dependencies using uv:

`uv sync --dev`

Then activate the environment:

`source .venv/bin/activate`

You also need to install a couple of npm dependencies. Make sure you install node, npm, and nvm in your 
machine, then run the following command to install and use the right version of node for this project:

```nvm install 18.0.0```

and

```nvm use 18.0.0```

Then install the npm dependencies:

```npm install @stoplight/spectral```

and

```npm install @stoplight/spectral```

Or if you prefer to use yarn:

```yarn add @stoplight/spectral```

and

```yarn add @stoplight/spectral```

Now you are ready to run the tests.

## Running the API server

To run the schemathesis tests, you need to run the API server locally.

To run the API server, you need a postgres database. I recommend you run it with Docker. Download 
Docker for desktop, and run the following command to start up the postgres database container:

```docker run -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres```

Then use the following command to run the API server:

```uvicorn server:server --reload```

You can now run the schemathesis tests against this server following the steps described in the 
chapter.

To run the pytest suite, follow the steps described in the chapter.
