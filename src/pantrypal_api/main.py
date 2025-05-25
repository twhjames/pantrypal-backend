from fastapi import FastAPI

app = FastAPI(
    title="PantryPal API",
    description="Smart pantry assistant backend with inventory, "
    + "recipe, and chatbot support",
    version="1.0.0",
)


# Health check route
@app.get("/", tags=["Health"])
def root():
    return {"message": "PantryPal API is running"}
