from pprint import pprint
from typing import Any
import dill
from result import Err, Ok, Result


def set_key(d: dict, keys: str, value: str):
    keys = keys.split(":")

    for i, key in enumerate(keys):
        if key not in d:
            if not i == len(keys) - 1:
                d.setdefault(key, {})
            else:
                d.setdefault(key, value)
        elif i == len(keys) - 1:
            d.pop(key)
            d.setdefault(key, value)
        d = d[key]


def get_key(d: dict, keys: str):
    keys = keys.split(":")
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            return d[key]

        d = d[key]


def delete_key(d: dict, keys: str):
    keys = keys.split(":")
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            del d[key]
            break
        d = d[key]


class JokeDB:
    def __init__(self) -> None:
        self._db = {}

    def __repr__(self) -> str:
        return str(self._db)

    def set(self, path: str, value: Any) -> dict[str, Any]:
        set_key(self._db, path, value)
        return self._db

    def get(self, path: str):
        return get_key(self._db, path)

    def delete(self, path: str):
        delete_key(self._db, path)
        return self._db

    def save(self, path: str) -> Result[None, Exception]:
        try:
            with open(path, "wb") as f:
                dill.dump(self._db, f)
        except Exception as e:
            return Err(e)
        return Ok(None)

    def load(self, path: str) -> Result[None, Exception]:
        try:
            with open(path, "rb") as f:
                self._db = dill.load(f)
        except Exception as e:
            return Err(e)
        return Ok(None)


if __name__ == "__main__":
    db = JokeDB()
    while True:
        command = input(">")
        tokens = command.split(" ")

        if tokens[0] == "SET":
            print(db.set(tokens[1], eval(" ".join(tokens[2:]))))

        elif tokens[0] == "GET":
            print(db.get(tokens[1]))

        elif tokens[0] == "DEL":
            db.delete(tokens[1])
            pprint(db)
        elif tokens[0] == "SAVE":
            db.save(tokens[1])
            print(f"Saved successfully to {tokens[1]}.")
        elif tokens[0] == "LOAD":
            db.load(tokens[1])
            print(f"Loaded successfully from {tokens[1]}.")
        elif tokens[0] == "EXIT":
            quit(0)
        else:
            print("Invalid command.")
