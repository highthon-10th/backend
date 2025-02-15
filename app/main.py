from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .routers.auth import router as auth_router
from .routers.items import router as items_router
from .routers.events import router as events_router
from .routers.visits import router as visits_router
from .database import init_db, close_db

app = FastAPI(title="FastAPI MongoDB JWT")

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(visits_router, prefix="/visits", tags=["visits"])

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI MongoDB JWT API"}

# Serve favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)