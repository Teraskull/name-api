from fastapi import FastAPI, HTTPException
from random import choice
import uvicorn
import json


app = FastAPI(
    title="Name API",
    description="",
    version="1.0.0",
)


with open('male-names.json') as jsonfile:
    male_names: list = json.load(jsonfile)

with open('female-names.json') as jsonfile:
    female_names: list = json.load(jsonfile)

all_names: list = sorted(male_names + female_names)


@app.get("/api/names/{sex}")
def names_all(sex: str):
    """Get all names.

    Args:
        sex (str): male/female/all

    Returns:
        dict: All names for given sex.
    """
    if sex == "male":
        names = male_names
    elif sex == "female":
        names = female_names
    elif sex == "all":
        names = all_names
    else:
        raise HTTPException(status_code=404, detail="not found")

    data = {
        "names": names
    }
    return data


@app.get("/api/name/{sex}/random")
def name_random(sex: str):
    """Get random name.

    Args:
        sex (str): male/female/all

    Returns:
        dict: Name object.
    """
    if sex == "male":
        names = male_names
    elif sex == "female":
        names = female_names
    elif sex == "all":
        names = all_names
    else:
        raise HTTPException(status_code=404, detail="not found")

    random_name = choice(names)
    name_index = names.index(random_name)
    data = {
        "name": random_name,
        "id": name_index
    }
    return data


@app.get("/api/name/{sex}")
def name_by_arg(sex: str, name: str = None, id: int = None):
    """Get name object by passed `name` or `id` argument.

    Args:
        sex (str): male/female/all

    Returns:
        dict: Name object if successful, otherwise error.
        If no argument passed, return all names.
    """
    if sex == "male":
        names = male_names
    elif sex == "female":
        names = female_names
    elif sex == "all":
        names = all_names
    else:
        raise HTTPException(status_code=404, detail="not found")

    if name:
        try:
            name_id = names.index(name.title())
            selected_name = names[name_id]
        except ValueError:
            raise HTTPException(status_code=404, detail="name not found")
        data = {
            "name": selected_name,
            "id": name_id
        }
        return data

    elif id:
        try:
            name = names[id]
        except IndexError:
            raise HTTPException(status_code=404, detail="id not found")
        except ValueError:
            raise HTTPException(status_code=400, detail="invalid id")
        data = {
            "name": name,
            "id": id
        }
        return data

    raise HTTPException(status_code=400, detail="Missing parameter id/name")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
