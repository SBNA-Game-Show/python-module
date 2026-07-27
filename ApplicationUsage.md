# Steps to Follow to use the Application Various Ways

This document explains how to set up and run the application in a local development environment using Docker.

---

## Local Development Setup

## Requirements

    Before running the application locally, ensure the following are installed:

    - Python version **3.11 or greater**
    - Docker installed and running
    - Git installed
    - Repository cloned locally
    - Repository opened in VS Code
    - `.env` file configured with required application settings

    Example `.env` file:

    ```env
    PORT=5100
    ATLAS_URI=<mongodb-atlas-connection-string>
    ```

## Commands

- Open terminal in your editor
- Run `cd docker.dev`
- Run `docker compose build --no-cache`
- Wait for the container to be built
- Run `docker compose up --build`
- The Flask server will run on port: 5100
- Documentation and API docs can be accessed via **http://localhost:5100**

## API Version

- The API version can directly be called by sending an HTTP/HTTPS request to the designated URLs provided in the API documentation.

## TO Detach it and use it with other applications

- Change the `ATLAS_URI` in Render to the desired `ATLAS_URI`.

## Word Complex plus other Application

- Initialize the MongoDB URI with a different name in the `.env` file of the other application.
- Open `config/dbconfig` and configure to accommodate both the databases for both Word Complex and other applications.
- Open Render and initialize the new MongoDB URI along with the existing `ATLAS_URI`.

**NOTE** - This project is currently configured to be deployed in two spaces: the `main` branch is deployed to Hugging Face (which serves as a temporary account), and the `master` branch is deployed to Render.

## To deploy to hugging face space using docker

- Create a Hugging Face Space using the Docker SDK.
- Inside the newly created Space, create an Access Token named `GITHUB` and replace the current `HF_TOKEN` with this new one.
- Open `.github/sync-to-hugging-face.yml` and replace the last push link with the new Space name and leaving the rest to same.
