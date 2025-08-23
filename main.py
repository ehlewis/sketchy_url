import os
import uvicorn
import random
import sqlite3
import jsonify
import db_functions
from typing import Any
from fastapi_throttle import RateLimiter
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, Body
from fastapi.responses import RedirectResponse, FileResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler

SEPERATORS = ["_", "-", ".", "$", "*", "%", "^", "!"]
EXTENSIONS = [".exe", ".7z", ".tar", ".dmg", ".clickme" , ".doc", ".docx", ".xls", ".xlsx", 
              ".ppt", ".pptx", ".docm", ".xlsm", ".pptm", ".com", ".scr", ".msi", ".vbs", 
              ".js", ".wsf", ".ps1", ".lnk"]

# ============== Setup ===============

connection = sqlite3.connect('sketchy_links.db', check_same_thread=False)
cursor = connection.cursor()
db = db_functions.DB(connection, cursor)
print("[+] Database connection established")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    # repeat task every day
    scheduler.add_job(func=db.clean_db, trigger='interval', days=1)
    scheduler.start()
    yield
    scheduler.stop()

app = FastAPI(lifespan=lifespan)
scheduler = AsyncIOScheduler()

# Limit to 5 requests per minute
limiter = RateLimiter(times=5, seconds=60)

# ============== Helpers =============
def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def random_case(word, chance=0.9):
    char_list = list(word)
    for z in range(0, len(word)):
        if random.random()>chance:
            char_list[z] = word[z].upper()
    return "".join(char_list)

def create_sketchy_path(wordlist, depth_range=[4,7], keyword_range=[1,5]):
    sketchy_url = ""
    wordlist_len = len(wordlist)
    depth = random.randint(depth_range[0], depth_range[1])
    #print("depth - " + str(depth))
    
    # Depth loop
    for i in range(0, depth):
        if i > 0:
            sketchy_url += "/"
        keyword_length = random.randint(keyword_range[0],keyword_range[1])
        #print("length - " + str(keyword_length))
        for n in range(0, keyword_length):
            word_choice = wordlist[random.randint(0, wordlist_len-1)]
            # Throw in some capitalization
            word_choice = random_case(word_choice)
            sketchy_url += word_choice
            #print(word_choice)
            chosen_seperator = SEPERATORS[random.randint(0,len(SEPERATORS)-1)]
            #print(chosen_seperator)
            if n < keyword_length-1:
                sketchy_url += chosen_seperator
    extension = EXTENSIONS[random.randint(0,len(EXTENSIONS)-1)]
    sketchy_url += extension
    return(sketchy_url)

# =============== Endpoints ===================
@app.get("/")
async def read_index():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/qr.html")
async def read_index():
    return FileResponse(os.path.join("static", "qr.html"))

@app.get("/clientinfo")
def clientinfo(request):
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    headers = dict(request.headers)
    return jsonify({
        "ip": client_ip,
        "headers": headers
    })

@app.post("/create_url", dependencies=[Depends(limiter)])
async def create_sketchy_url(body: Any = Body(...)):
    sketchy = create_sketchy_path(wordlist)
    db_added = db.add_link_to_db(sketchy,body["url"])
    if db_added == "ok":
        return {"status": "created", "url": "/"+sketchy}
    return {"status": "error"}


@app.api_route("/{full_path:path}")
def resolve_sketchy_url(full_path: str):
    print("Full path: " + str(full_path))
    real_url = db.fetch_real_url_from_db(full_path)
    print(real_url)
    if real_url:
        return RedirectResponse(url=real_url, status_code=status.HTTP_302_FOUND)
    return FileResponse(os.path.join("static", "404.html"))



# =============== Main ========================

wordlist = read_file("resources/wordlist.txt")

db.create_link_table()

'''
for x in range(0,15):
    print(create_sketchy_path(wordlist))
    print("\n\n")


sketchy_url = "c1ick^limited-accesS%user$Getpaid/signinportal/confirm*l0g1n*l0gin%customer/personnel^passwORD"
real_url = "https://www.google.com/"
add_link_to_db(sketchy_url, real_url)
'''

uvicorn.run(app, host="0.0.0.0", port=8000)

print("Shutting down")

connection.close()
scheduler.shutdown()



'''
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''