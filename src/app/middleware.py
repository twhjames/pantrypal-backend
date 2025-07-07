from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI):
    # allow_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
