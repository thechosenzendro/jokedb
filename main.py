from jokedb import JokeDB


cache = JokeDB()

cache.set("Hello:World", "Hi!")
print(cache.get("Hello:World"))
cache.save("dev.jokedb")
