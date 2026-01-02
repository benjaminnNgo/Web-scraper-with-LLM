#Docker build
docker build -t fastapi-app .

#Launch the app
docker run -p 8000:8000 fastapi-app

