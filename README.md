# CDN Integration Prototype Using Kong API Gateway and Python

## Overview

This repository contains a prototype that demonstrates the integration of a Content Delivery Network (CDN) using Kong API Gateway and Python. The prototype includes the setup instructions, URLs for accessing different services, and steps for testing the CDN functionality.

## Kong Gateway is a lightweight, fast, and flexible cloud-native API gateway. 

An API gateway is a reverse proxy that lets you manage, configure, and route requests to your APIs. Kong Gateway runs in front of any RESTful API and can be extended through modules and plugins. It’s designed to run on decentralized architectures, including hybrid-cloud and multi-cloud deployments.

There are two options such as db-less and with database(postgres) to install KONG. We will take db-less mode. DB-less mode is a simpler mode that does not require a database. This can be a good option since this is a simple task so we can avoid the complexity of setting up and managing a database. However, DB-less mode has some limitations. For example, we cannot use Kong's built-in caching features in DB-less mode.Since in the task mentioned without caching mechanism so we can pick DB-less mode.

## Setup Instructions

1. **Clone the Repository:** Start by cloning this repository to your local machine:

    ```sh
    git clone https://github.com/Mashfiqur/kong-prototype.git
    ```
    ```sh
    cd kong-prototype
    ```

2. **Environment Configuration:** Copy the environment file and configure it if necessary:

    ```sh
    cp .env.example .env
    ```

3. **Docker compose Configuration:** Copy the docker-compose YAML file and configure it if necessary:

    ```sh
    cp docker-compose-example.yaml docker-compose.yaml
    ```

4. **Create Docker Network:** Create a Docker network for the services:

    ```sh
    docker network create kong-cdn-net
    ```

5. **Build Docker Services:** Build the Docker services using the provided `docker-compose.yaml` file:

    ```sh
    docker-compose up --build
    ```
### We will build three images such as kong, cdn, app under kong-cdn-net docker network through docker-compose.yaml file. Available URL(s) after building the services through docker-compose.yaml file

## Service URLs

- **KONG Admin URL:** [http://localhost:8001](http://localhost:8001)
- **KONG API Gateway URL:** [http://localhost:8000](http://localhost:8000)

- **App Microservice:** [http://localhost:5000](http://localhost:5000)
- **App Microservice URL through KONG:** [http://localhost:8000/app](http://localhost:8000/app) or [http://kong:8000/app](http://kong:8000/app) (Inside Docker network)

- **CDN Microservice:** [http://localhost:5001](http://localhost:5001)
- **CDN Microservice URL through KONG:** [http://localhost:8000/cdn](http://localhost:8000/cdn) or [http://kong:8000/cdn](http://kong:8000/cdn) (Inside Docker network)

## Testing the Prototype

### Upload Mechanism

1. Open Postman.
2. Make a POST request to one of the following URLs:
   - [http://localhost:8000/app/upload](http://localhost:8000/app/upload) (With the help of KONG ADMIN URL. This will forward to app service as we mentioned in the kong.yaml configuration file.)
   - [http://localhost:5000/upload](http://localhost:5000/upload) (Through app service base URL)
3. Set the `Content-Type` header to `multipart/form-data`.
4. Attach a file using the appropriate key('file').
5. The service will store the file in the `cdn/assets` directory and generate a unique URL for the asset.
6. You can hit the generated URL which you will find in the response in the browser or Postman to see 
   the stored file

### Retrieve Mechanism

1. Open Postman.
2. Make a GET request to one of the following URLs:
   - [http://localhost:8000/app/retrieve/{fileName}](http://localhost:8000/app/retrieve/{fileName}) (With the help of KONG ADMIN URL. This will forward to app service as we mentioned in the kong.yaml configuration file.)
   - [http://localhost:5000/retrieve/{fileName}](http://localhost:5000/retrieve/{fileName}) (Through app service base URL).
3. Replace `{fileName}` with the actual filename.
4. If the file exists in the assets folder inside cdn directory, the service will generate a 
   unique URL for the asset and send as response.

## Additional Notes

- Use the provided Kong Admin URLs to check routes, services, and endpoints of the Kong API Gateway through these URL.

1. http://localhost:8001/routes (Checking Routes)
2. http://localhost:8001/services (Checking Services)
3. http://localhost:8001/endpoints (Checking Endpoints)

## Conclusion

This prototype showcases the integration of a CDN using Kong API Gateway and Python. By following the setup instructions and testing the upload and retrieval mechanisms, you can assess the functionality of Kong as a reverse proxy for CDN operations. If you encounter any issues or need further assistance, please refer to the provided documentation or seek help from me.