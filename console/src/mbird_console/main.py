from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mbird_console.api import routes

app = FastAPI(title="mbird Console API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.get("/")
async def root():
    return {"message": "mbird Console API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
