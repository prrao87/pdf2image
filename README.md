1. Run the server in dev mode:
   `uv run dotenv run fastapi dev app/main.py`
   You can remove `dotenv run` from the command if you use `load_dotenv()` inside your python file, before baml_client is imported.

Run in prod
`uv run fastapi run app/main.py`

Docker build:
`docker build -t fastapi-app .`

Run container:
`docker run -p 8000:8000 fastapi-app`

Curl the endpoint:
`curl -X POST -H "Content-Type: multipart/form-data" -F "files=@files/images/invoice.png" http://localhost:8000/extract/`

You must have files/images/invoice.png present in the directory from where you run this.
