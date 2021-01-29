from pathlib import Path



database_folder = Path(__file__).resolve().parent / Path("anime_database")
anime_folder = database_folder / Path("Anime")
people_folder = database_folder / Path("People")
staff_folder = database_folder / Path("Staff")


resource_types = {
    "anime" : anime_folder,
    "people" : people_folder,
    "staff" : staff_folder
}