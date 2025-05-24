from fastapi import FastAPI
from hims_api.routers import items as pantry_routes

app = FastAPI()

# Register pantry item routes
app.include_router(pantry_routes.router, prefix="/pantry", tags=["Pantry"])

@app.get("/")
def root():
    return {"message": "Welcome to PantryPal API"}
