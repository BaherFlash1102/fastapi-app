from fastapi import FastAPI
import redis
import psycopg2
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI app is running!"}

@app.get("/db-check")
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        return {"db_status": "connected"}
    except Exception as e:
        return {"db_status": "error", "details": str(e)}

@app.get("/cache-check")
def cache_check():
    try:
        r = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379)
        r.set("test", "ok")
        return {"cache_status": "connected", "value": r.get("test").decode()}
    except Exception as e:
        return {"cache_status": "error", "details": str(e)}
