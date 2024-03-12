import redis
from redis_lru import RedisLRU

from models import Author, Quote


client = redis.StrictRedis(host = "localhost", port = 6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_author(name):
    print(f"Quotes of '{name}':") 
    authors = Author.objects(fullname__istartswith=name) 
    result = {}
    if authors:        
        for a in authors:
            quotes = Quote.objects(author=a)
            result[a.fullname] = [q.quote for q in quotes]
            return result
    else:
        return "Nothing found!"   
        

@cache
def find_by_tag(tags):
    print(f"Quotes containing '{tags}':")
    result = set()
    for tag in tags.split(","):                     
        quotes = Quote.objects(tags__iregex=tag.strip())
        if quotes:
            for q in quotes:
                result.add(f'{q.author.fullname} : {q.quote}')
    if result:
        return result
    else:
        return "Nothing found!"   
    


def  main():
        
    while True:
        command = input("Enter command <name | tag | tags>: <name | tag | tag1,tag2> or 'exit' >>> ")
        command.strip().lower()
        
        
        if command.startswith("exit"):
            print("Goodbye")            
            break

        if command.startswith("name"):
            name = command.split(":")[1].strip()
            print(find_by_author(name))
            

        if command.startswith("tag"):
            tags = command.split(":")[1].strip()
            print(find_by_tag(tags))
            
            
        
    

if __name__ == "__main__":
    main()