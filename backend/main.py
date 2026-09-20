from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import todos, conflict_logs
from .db import init_db

# Initialize the database
init_db()

app = FastAPI(
    title="Todo Sync API",
    description="A real-time Todo synchronization API with conflict resolution",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Todo Sync API"}

# Include routers
app.include_router(todos.router)
app.include_router(conflict_logs.router)

@app.on_event("startup")
async def startup_event():
    print("Todo Sync application started")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}