import random
import sqlite3
import jsonify
from fastapi import FastAPI, Request

SEPERATORS = ["_", "-", ".", "$", "*", "%", "^", "!"]

# ============== Setup ===============

connection = sqlite3.connect('sketchy_links.db')
cursor = connection.cursor()
print("[+] Database connection established")

app = FastAPI()

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
        
    return(sketchy_url)
    
# ------ DB Helper funtctions ---------

def create_link_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Links (
        sketchy TEXT NOT NULL PRIMARY KEY,
        real TEXT NOT NULL,
        creation_date INTEGER
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'Links' created successfully!")

def add_link_to_db(real_url, sketchy_url):
    pass

def fetch_real_url_from_db(sketchy_url):
    pass

def clean_db():
    pass


# =============== Endpoints ===================
@app.get("/qr")
def qr_page():
    pass

@app.get("/clientinfo")
def clientinfo(request):
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    headers = dict(request.headers)
    return jsonify({
        "ip": client_ip,
        "headers": headers
    })

@app.post("/create_url")
def create_sketchy_url():
    pass

@app.route("/{full_path:path}")
def resolve_sketchy_url(request: Request, full_path: str):
    pass



# =============== Main ========================

wordlist = read_file("resources/wordlist.txt")

create_link_table()

for x in range(0,15):
    print("http://zx6ui.lol" + create_sketchy_path(wordlist))
    print("\n\n")


connection.close()