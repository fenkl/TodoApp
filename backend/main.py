from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import todos, conflict_logs
from .db import init_db

app = FastAPI(
    title="Todo Sync API",
    description="API for Todo Sync application with cross-platform synchronization",
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

# Include routers
app.include_router(todos.router, prefix="/api/v1/todos", tags=["todos"])
app.include_router(conflict_logs.router, prefix="/api/v1/conflict-logs", tags=["conflict-logs"])

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Todo Sync API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}