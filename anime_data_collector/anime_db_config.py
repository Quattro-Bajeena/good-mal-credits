from pathlib import Path
import os

#print("anime config", Path(__name__).resolve())

#database_folder = Path(__file__).resolve().parent / Path("anime_database")
database_folder = Path("anime_database")
anime_folder = database_folder / Path("Anime")
people_folder = database_folder / Path("People")
characters_staff_folder = database_folder / Path("Characters_Staff")
characters_folder = database_folder / Path('Characters')
manga_folder = database_folder / Path('Manga')
studios_folder = database_folder / Path('Studios')




resource_types = {
    "anime" : anime_folder,
    "people" : people_folder,
    "characters_staff" : characters_staff_folder,
    "characters" : characters_folder,
    'manga' : manga_folder,
    'studios' : studios_folder,
}


images_folders = {
    'anime' : database_folder / 'images' / 'anime',
    'people' : database_folder /'images' / 'people',
    'characters' : database_folder /'images' / 'characters',
    'manga' : database_folder /'images' / 'manga'
}

def config_database(main_folder : Path):
    global database_folder, anime_folder, people_folder, characters_folder, resource_types,characters_staff_folder, manga_folder, studios_folder, images_folders


    database_folder = main_folder / Path("anime_database")
    anime_folder = database_folder / Path("Anime")
    people_folder = database_folder / Path("People")
    characters_staff_folder = database_folder / Path("Characters_Staff")
    characters_folder = database_folder / Path('Characters')
    manga_folder = database_folder / Path('Manga')
    studios_folder = database_folder / Path('Studios')


    images_folders['anime'] =  main_folder / 'static' / 'images' / 'anime'
    images_folders['people'] = main_folder / 'static' / 'images' / 'people'
    images_folders['characters'] = main_folder / 'static' / 'images' / 'characters'
    images_folders['manga'] = main_folder / 'static' / 'images' / 'manga'

    resource_types = {
        "anime" : anime_folder,
        "people" : people_folder,
        "characters_staff" : characters_staff_folder,
        "characters" : characters_folder,
        'manga' : manga_folder,
        'studios' : studios_folder,
    }

    if not database_folder.is_dir():
        os.mkdir(database_folder)
        os.mkdir(anime_folder)
        os.mkdir(people_folder)
        os.mkdir(characters_staff_folder)
        os.mkdir(characters_folder)
        os.mkdir(manga_folder)
        os.mkdir(studios_folder)
        #print("anime db config - created folders")
    else:
        # print("anime db config - folders exists")
        pass


