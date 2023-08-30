docker network create kong-cdn-net
docker-compose up --build

POST REQUEST
http://localhost:8000/app/upload
Content-Type: multipart/form-data
file: Upload a file

You will get an URL in the response. You can see the file through hitting the URL on browser or Postman

