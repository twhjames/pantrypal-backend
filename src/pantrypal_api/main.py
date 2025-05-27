from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.pantrypal_api.chatbot.routers import chatbot_router

# Initialize the FastAPI app with metadata for automatic Swagger docs
app = FastAPI(
    title="PantryPal API",
    description="Smart pantry assistant backend with inventory, recipe, and chatbot support",
    version="1.0.0",
)

# Add CORS middleware to allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check route
@app.get("/", tags=["Health"])
def root():
    return {"message": "PantryPal API is running"}


# Register routes
app.include_router(chatbot_router.router)
