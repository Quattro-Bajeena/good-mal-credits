from pathlib import Path
import os

#print("anime config", Path(__name__).resolve())

#database_folder = Path(__file__).resolve().parent / Path("anime_database")
database_folder = Path("anime_database")
anime_folder = database_folder / Path("Anime")
people_folder = database_folder / Path("People")
staff_folder = database_folder / Path("Staff")
characters_folder = database_folder / Path('Characters')
anime_characters_folder = database_folder / Path("Anime_Characters")


resource_types = {
    "anime" : anime_folder,
    "people" : people_folder,
    "staff" : staff_folder,
    "characters" : characters_folder,
    "anime_characters" : anime_characters_folder
}


def config_database(main_folder : Path):
    global database_folder, anime_folder, people_folder, staff_folder, characters_folder, anime_characters_folder, resource_types


    database_folder = main_folder / Path("anime_database")
    anime_folder = database_folder / Path("Anime")
    people_folder = database_folder / Path("People")
    staff_folder = database_folder / Path("Staff")
    characters_folder = database_folder / Path('Characters')
    anime_characters_folder = database_folder / Path("Anime_Characters")

    resource_types = {
        "anime" : anime_folder,
        "people" : people_folder,
        "staff" : staff_folder,
        "characters" : characters_folder,
        "anime_characters" : anime_characters_folder
    }

    if not database_folder.is_dir():
        os.mkdir(database_folder)
        os.mkdir(anime_folder)
        os.mkdir(people_folder)
        os.mkdir(staff_folder)
        os.mkdir(characters_folder)
        os.mkdir(anime_characters_folder)
        #print("anime db config - created folders")
    else:
        pass
        #print("anime db config - folders exists")


