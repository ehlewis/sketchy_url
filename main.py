import random
#import fastapi


SEPERATORS = ["_", "-", ".", "$", "*", "%"]


def random_case(word, chance=0.9):
    char_list = list(word)
    for z in range(0, len(word)):
        if random.random()>chance:
            char_list[z] = word[z].upper()
    return "".join(char_list)

def create_sketchy_path(wordlist, depth_range=[4,7], keyword_range=[1,5] ):
    sketchy_url = "/"    
    wordlist_len = len(wordlist)
    depth = random.randint(depth_range[0], depth_range[1])
    #print("depth - " + str(depth))
    
    # Depth loop
    for i in range(0, depth):
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
            sketchy_url += chosen_seperator
        sketchy_url += "/"
    print(sketchy_url)
    

def add_link_to_db(real_url, sketchy_url):
    pass


def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

wordlist = read_file("resources/wordlist.txt")

for x in range(0,15):
    print(create_sketchy_path(wordlist))
    print("\n\n")
