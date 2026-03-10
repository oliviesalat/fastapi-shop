from fastapi import FastAPI, HTTPException, Depends
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import products, categories, cart
from .database import init_db, get_db
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Starting application...")
    yield
    print("Application stopped")

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/static', StaticFiles(directory=settings.static_dir), name='static')
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(cart.router)

@app.get('/')
def root():
    return {
        'message': 'hello',
        'docs': 'api/docs',
    }

@app.get('/healthcheck')
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {'status': 'healthy'}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")

