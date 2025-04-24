# main.py
import datetime
import shortuuid # type: ignore
from fastapi import FastAPI, HTTPException, Request # type: ignore
from fastapi.responses import RedirectResponse
from database import database, engine, metadata
from models import links
from fastapi.middleware.cors import CORSMiddleware
from datetime import timezone


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# @app.post("/shorten")
# async def shorten_url(original_url: str):
#     short_code = shortuuid.ShortUUID().random(length=6)
#     query = links.insert().values(original_url=original_url, short_url=short_code)
#     await database.execute(query)
#     return {"short_url": f"http://localhost:8000/u/{short_code}"}

@app.post("/shorten")
async def shorten_url(original_url: str):
    short_code = shortuuid.ShortUUID().random(length=6)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 7 days expiration
    query = links.insert().values(
        original_url=original_url,
        short_url=short_code,
        created_at=datetime.datetime.utcnow(),
        expiration_date=expiration,
        clicks=0
    )
    await database.execute(query)
    return {"short_url": short_code}


# @app.get("/u/{short_url}")
# async def redirect_to_original(short_url: str):
#     print("Received short_url:", short_url)
#     query = links.select().where(links.c.short_url == short_url)
#     result = await database.fetch_one(query)
#     print("DB result:", result)
#     print("result:", query)
#     if result:
#         return {"original_url": result["original_url"]}
#     else:
#         raise HTTPException(status_code=404, detail="URL not found")


@app.get("/u/{short_url}")
async def redirect_to_original(short_url: str, request: Request):
    query = links.select().where(links.c.short_url == short_url)
    result = await database.fetch_one(query)
    if result:
        expiration_date = result["expiration_date"]
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        if expiration_date and expiration_date < now_utc:
            raise HTTPException(status_code=410, detail="Link expired")  # 410 Gone

        # Update click count
        update_query = links.update().where(links.c.short_url == short_url).values(clicks=result["clicks"] + 1)
        await database.execute(update_query)

        original_url = result["original_url"]
        accept_header = request.headers.get("accept", "")
        print(f"Accept header: {accept_header}")

        # If client wants JSON (Swagger or API call)
        if "application/json" in accept_header:
            return {"original_url": original_url}
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")


@app.get("/info/{short_url}")
async def get_url_info(short_url: str):
    """Extra API to see clicks, created time etc"""
    query = links.select().where(links.c.short_url == short_url)
    result = await database.fetch_one(query)
    if result:
        created_at = result["created_at"].strftime("%d-%m-%Y %I:%M:%S %p")
        expiration_date = result["expiration_date"].strftime("%d-%m-%Y %I:%M:%S %p")
        return {
            "original_url": result["original_url"],
            "created_at": created_at,
            "expiration_date": expiration_date,
            "clicks": result["clicks"],
        }
    else:
        raise HTTPException(status_code=404, detail="URL not found")


