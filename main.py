import uvicorn

if __name__ == "__main__":
    uvicorn.run("cookery.api:api", reload=True)