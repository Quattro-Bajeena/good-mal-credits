import datetime

from flask_sqlalchemy import SQLAlchemy
from celery.app.task import Task

from anime_credits_app import db, adc, log_n_cache
from anime_credits_app.models import Anime, Person, Character, StaffMember, VoiceActor, Studio, Manga, MangaAuthor



mal = adc.mal

class StatusUpdater():
    def __init__(self, total_progress:int, celery_task : Task):
        self.current_progess = 0
        self.total_progress = total_progress
        self.celery_task = celery_task

    def update_status(self, status:tuple, add_progress = True):
        if add_progress:
            self.current_progess += 1

        if type(status) == tuple or type(status) == list:
            status = '\n'.join(status)
        

        message = {
            'current': self.current_progess,
            'total' : self.total_progress,
            'status' : status
        }
        self.celery_task.update_state(state='PROGRESS', meta=message)
        print(message)



def update_function_status(status, current_progess:int, total_progress:int, celery_task : Task):

    if type(status) == tuple:
        status = '\n'.join(status)

    message = {
        'current': current_progess,
        'total' : total_progress,
        'status' : status
    }
    celery_task.update_state(state='PROGRESS', meta=message)
    print(message)


def add_anime(anime : dict) -> Anime:

    anime_db = Anime(
            mal_id = anime['mal_id'],
            url = anime['url'],
            image_url = anime['image_url'],
            title = anime['title'],
            title_english = anime['title_english'],
            title_japanese = anime['title_japanese'],
            format_type = anime['type'],
            source = anime['source'],
            episodes = anime['episodes'],
            status = anime['status'],
            aired_from = datetime.datetime.strptime(anime['aired']['from'][:10],
                '%Y-%m-%d') if anime['aired']['from'] else None,
            aired_to = datetime.datetime.strptime(anime['aired']['to'][:10],
                '%Y-%m-%d') if anime['aired']['to'] else None,
            score = anime['score'],
            scored_by = anime['scored_by'],
            rank = anime['rank'],
            popularity = anime['popularity'],
            members = anime['members'],
            favorites = anime['favorites'],
            premiered = anime['premiered']
        )
    #print(f"new anime db created - {anime['title']}")
    db.session.add(anime_db)
    return anime_db

def update_anime(anime_db : Anime, anime : dict):
    anime_db.url = anime['url']
    anime_db.image_url = anime['image_url']
    anime_db.title = anime['title'],
    anime_db.title_english = anime['title_english']
    anime_db.title_japanese = anime['title_japanese']
    anime_db.format_type = anime['type']
    anime_db.source = anime['source']
    anime_db.episodes = anime['episodes']
    anime_db.status = anime['status']
    anime_db.aired_from = datetime.datetime.strptime(anime['aired']['from'][:10],'%Y-%m-%d') if anime['aired']['from'] else None
    anime_db.aired_to = datetime.datetime.strptime(anime['aired']['to'][:10], '%Y-%m-%d') if anime['aired']['to'] else None
    anime_db.score = anime['score']
    anime_db.scored_by = anime['scored_by']
    anime_db.rank = anime['rank']
    anime_db.popularity = anime['popularity']
    anime_db.members = anime['members']
    anime_db.favorites = anime['favorites']
    anime_db.premiered = anime['premiered']
        

def add_manga(manga : dict) -> Manga:
    manga_db = Manga(
        mal_id = manga['mal_id'],
        url = manga['url'],
        title = manga['title'],
        title_english = manga['title_english'],
        title_japanese = manga['title_japanese'],
        image_url = manga['image_url'],
        status = manga['status'],
        work_type = manga['type'],
        volumes = manga['volumes'],
        chapters = manga['chapters'],
        publishing = manga['publishing'],
        published_from = datetime.datetime.strptime(manga['published']['from'][:10],'%Y-%m-%d') if manga['published']['from'] else None,
        published_to = datetime.datetime.strptime(manga['published']['to'][:10],'%Y-%m-%d') if manga['published']['to'] else None,
        rank = manga['rank'],
        score = manga['score'],
        scored_by = manga['scored_by'],
        popularity = manga['popularity'],
        members = manga['members'],
        favorites = manga['favorites'],
        serialization = manga['serializations'][0]['name'] if len(manga['serializations'])>0 else None
    )
    #print(f"new manga created - {manga_db.title}")
    db.session.add(manga_db)
    return manga_db

def update_manga(manga_db : Manga, manga : dict):
    manga_db.mal_id = manga['mal_id']
    manga_db.url = manga['url']
    manga_db.title = manga['title']
    manga_db.title_english = manga['title_english']
    manga_db.title_japanese = manga['title_japanese']
    manga_db.image_url = manga['image_url']
    manga_db.status = manga['status']
    manga_db.work_type = manga['type']
    manga_db.volumes = manga['volumes']
    manga_db.chapters = manga['chapters']
    manga_db.publishing = manga['publishing']
    published_from = datetime.datetime.strptime(manga['published']['from'][:10],'%Y-%m-%d') if manga['published']['from'] else None
    manga_db.published_to =  published_to = datetime.datetime.strptime(manga['published']['to'][:10],'%Y-%m-%d') if manga['published']['to'] else None
    manga_db.rank = manga['rank']
    manga_db.score = manga['score']
    manga_db.scored_by = manga['scored_by']
    manga_db.popularity = manga['popularity']
    manga_db.members = manga['members']
    manga_db.favorites = manga['favorites']
    manga_db.serialization = manga['serializations'][0] if len(manga['serializations'])>0 else None


def add_studio(studio : dict) -> Studio:
    studio_db = Studio(
        mal_id = studio['mal_id'],
        work_type = studio['type'],
        name = studio['name'],
        url = studio['url']
    )

    db.session.add(studio_db)
    #print(f"NEW STUDIO ADDED - {studio_db.name}", )
    return studio_db

def update_studio(studio_db : Studio, studio : dict):
    studio_db.work_type = studio['type']
    studio_db.name = studio['name']
    studio_db.url = studio['url']

def add_person(person : dict) -> Person:
    person_db = Person(
        mal_id = person['mal_id'],
        url = person['url'],
        image_url = person['image_url'],
        name = person['name'],
        given_name = person['given_name'],
        family_name = person['family_name'],
        birthday = datetime.datetime.strptime(person['birthday'][:10],'%Y-%m-%d') if person['birthday'] else None,
        member_favorites = person['member_favorites']
    )

    db.session.add(person_db)
    #print(f"added new person - {person['name']}")
    return person_db

def update_person(person_db : Person, person : dict):
    person_db.url = person['url']
    person_db.image_url = person['image_url']
    person_db.name = person['name']
    person_db.given_name = person['given_name']
    person_db.family_name = person['family_name']
    person_db.birthday = datetime.datetime.strptime(person['birthday'][:10],'%Y-%m-%d') if person['birthday'] else None
    person_db.member_favorites = person['member_favorites']


def add_staff_member(staff_id, anime:dict, person:dict, position) -> StaffMember:
    new_credit = StaffMember(
        id = staff_id,
        position = position,
        person_id = person['mal_id'],
        anime_id = anime['mal_id']
    )
    db.session.add(new_credit)
    #print(f"added new staff member: {staff_id}")
    return new_credit

def update_staff_member(staff_member_db : StaffMember, anime:dict, person:dict, position):
    staff_member_db.position = position
    staff_member_db.person_id = person['mal_id']
    staff_member_db.anime_id = anime['mal_id']

def add_voice_actor(voice_actor_id, anime : dict, person : dict, character : dict, role : dict) -> VoiceActor:

    language = None
    for voice_actor in character['voice_actors']:
        if voice_actor['mal_id'] == person['mal_id']:
            language = voice_actor['language']
            break

    voice_actor_db = VoiceActor(
        id = voice_actor_id,
        role = role,
        language = language,
        anime_id = anime['mal_id'],
        person_id = person['mal_id'],
        character_id = character['mal_id']
    )

    db.session.add(voice_actor_db)
    #print(f"added new voice actor {voice_actor_id}")
    return voice_actor_db

def update_voice_actor(voice_actor_db:VoiceActor, anime : dict, person : dict, character : dict, role : dict):

    language = None
    for voice_actor in character['voice_actors']:
        if voice_actor['mal_id'] == person['mal_id']:
            language = voice_actor['language']
            break

    voice_actor_db.role = role
    voice_actor_db.language = language,
    voice_actor_db.anime_id = anime['mal_id']
    voice_actor_db.person_id = person['mal_id']
    voice_actor_db.character_id = character['mal_id']

def add_character(character : dict) -> Character:
    character_db = Character(
        mal_id = character['mal_id'],
        url = character['url'],
        image_url = character['image_url'],
        name = character['name'],
        member_favorites = character['member_favorites']
    )

    db.session.add(character_db)
    #print(f"added new character: {character['name']}")
    return character_db

def update_character(character_db : Character, character : dict):
    character_db.url = character['url']
    character_db.image_url = character['image_url']
    character_db.name = character['name']
    character_db.member_favorites = character['member_favorites']

def add_manga_author(manga_author_id, manga:dict, person:dict, position) -> MangaAuthor:

    author_type = None
    for author in manga['authors']:
        if author['mal_id'] == person['mal_id']:
            author_type = author['type']

    manga_author_db = MangaAuthor(
        id = manga_author_id,
        position = position,
        author_type = author_type,
        person_id = person['mal_id'],
        manga_id = manga['mal_id']
    )
    db.session.add(manga_author_db)
    return manga_author_db

def update_manga_author(manga_author_db:MangaAuthor, manga:dict, person:dict, position):
    author_type = None
    for author in manga['authors']:
        if author['mal_id'] == person['mal_id']:
            author_type = author['type']

    manga_author_db.position = position
    manga_author_db.author_type = author_type
    manga_author_db.person_id = person['mal_id']
    manga_author_db.manga_id = manga['mal_id']


def get_anime_db(anime:dict,  use_cached:bool):
    mal_id = anime['mal_id']
    anime_db = Anime.query.get(mal_id)
    if not anime_db:
        anime_db = add_anime(anime)
    elif not use_cached:
        update_anime(anime_db, anime)
    return anime_db

def get_manga_db(manga:dict, use_cached:bool):
    mal_id = manga['mal_id']
    manga_db = Manga.query.get(mal_id)
    if not manga_db:
        manga_db = add_manga(manga)
    elif not use_cached:
        update_manga(manga_db, manga)
    return manga_db

def get_studio_db(studio:dict,  anime_db:Anime, use_cached:bool):
    mal_id = studio['mal_id']
    studio_db = Studio.query.get(mal_id)
    if not studio_db:
        studio_db = add_studio(studio)
    elif not use_cached:
        update_studio(studio_db, studio)

    studio_db.anime.append(anime_db)
    return studio_db


def get_person_db(person:dict, use_cached:bool):
    mal_id = person['mal_id']
    person_db = Person.query.get(mal_id)
    if not person_db:
        person_db = add_person(person)
    elif not use_cached:
        update_person(person_db, person)
    return person_db

def get_character_db(character:dict, anime_db:Anime, use_cached:bool):
    mal_id = character['mal_id']
    character_db = Character.query.get(mal_id)
    if not character_db:
        character_db = add_character(character)
        anime_db.characters.append(character_db)
    elif not use_cached:
        update_character(character_db, character)
    return character_db

def get_staff_member_db(anime:dict, person:dict, position:dict, person_db:Person, anime_db:Anime, use_cached:bool):
    staff_id = f"{anime['mal_id']}/{person['mal_id']}/{position}"
    staff_member_db = StaffMember.query.get(staff_id)
    if not staff_member_db:
        staff_member_db = add_staff_member(staff_id, anime, person, position)
        person_db.staff_credits.append(staff_member_db)
        anime_db.staff.append(staff_member_db)
    elif not use_cached:
        update_staff_member(staff_member_db, anime, person, position)
    return staff_member_db


def get_manga_author_db(manga:dict, person:dict, position, manga_db:Manga, person_db:Person, use_cached:bool):

    manga_author_id = f"{manga['mal_id']}/{person['mal_id']}/{position}"
    manga_author_db = MangaAuthor.query.get(manga_author_id)
    if not manga_author_db:
        manga_author_db = add_manga_author(manga_author_id, manga, person, position)

        person_db.published_manga.append(manga_author_db)
        manga_db.authors.append(manga_author_db)
    elif not use_cached:
        update_manga_author(manga_author_db, manga, person, position)

    return manga_author_db

def get_voice_actor_db(anime, person, character, role, anime_db, person_db, character_db, use_cached:bool):

    voice_actor_id = f"{anime['mal_id']}/{person['mal_id']}/{character['mal_id']}"
    voice_actor_db = VoiceActor.query.get(voice_actor_id)
    if not voice_actor_db:
        voice_actor_db = add_voice_actor(voice_actor_id, anime, person,character, role)
        anime_db.voice_actors.append(voice_actor_db)
        person_db.voice_acting_roles.append(voice_actor_db)
        character_db.voice_actors.append(voice_actor_db)
    elif not use_cached:
        update_voice_actor(voice_actor_db, anime, person, character, role)
    return voice_actor_db






# ---------------MAIN FUNCTIONS----------------

def update_characters_staff(anime_mal_id:int, use_cached:bool, celery_task : Task = None):
    print("update staff start")
    update_function_status("updating anime info", 0, 1, celery_task)

    # SETUP
    anime = mal.get_resource('anime', anime_mal_id, use_cached=use_cached)
    characters_staff = mal.get_resource('characters_staff', anime_mal_id, use_cached=use_cached) 
    staff = characters_staff['staff']
    characters = characters_staff['characters']
    

    anime_db = get_anime_db(anime, use_cached)
    print(f"UPDATING ANIME -------- {anime_db.title} -----------")

   

    total_progress = 1 + len(anime['studios']) + len(staff) + len(characters)
    for character_basic_info in characters:
        total_progress += len(character_basic_info['voice_actors'])

    status = StatusUpdater(total_progress, celery_task)
    status.update_status(("updating studios"))
    

    # STUDIOS
    for studio in anime['studios']:
        
        studio_db = get_studio_db(studio, anime_db, use_cached)

        status.update_status(("updating studios", f"{studio['name']}"))
        
        
    print("updated studios")
    status.update_status("updating staff", add_progress=False)

    # STAFF
    for staff_member in staff:
        person = mal.get_resource('people', staff_member['mal_id'], use_cached=use_cached)

        person_db = get_person_db(person, use_cached)

        for position in staff_member['positions']:
            
            staff_member_db = get_staff_member_db(anime, person, position, person_db, anime_db, use_cached)

        status.update_status(("updating staff", f"{person['name']}"))
                
    print("updated staff")
    status.update_status("updating characters", add_progress=False)

    # CHARACTERS
    for character_basic_info in characters:
        character = mal.get_resource('characters', character_basic_info['mal_id'], use_cached=use_cached)
        if not character:
            continue
        character_db = get_character_db(character, anime_db, use_cached)
        role = character_basic_info["role"]

        status.update_status(("updating character", f"{character['name']}"))

        for voice_actor in character_basic_info['voice_actors']:
            
            person = mal.get_resource('people', voice_actor['mal_id'],use_cached=use_cached)
            person_db = get_person_db(person, use_cached)
    
            voice_actor_db = get_voice_actor_db(anime, person, character, role, anime_db, person_db, character_db, use_cached)


            status.update_status(("updating character", f"{character['name']}", f"voice actor {person['name']}"))
            

        
    print("updated characters")
    update_function_status("finishing", 1, 1, celery_task )
    db.session.commit()







# ------------------------------------------------------------------------------------------
def update_person_credits(person_mal_id : int, use_cached:bool, celery_task:Task = None):
    print("update person credits start")
    update_function_status("updating person info", 0, 1, celery_task)

    person = mal.get_resource('people', person_mal_id, use_cached=use_cached)

    person_db = get_person_db(person, use_cached)

    print(f"UPDATING PERSON -------- {person_db.name} -----------")
    total_progress = 1 + 2 * len(person['voice_acting_roles']) + len(person['anime_staff_positions']) + len(person['published_manga'])
    status = StatusUpdater(total_progress, celery_task)
    status.update_status("updating voice acting roles")


    for role in person['voice_acting_roles']:
        
        anime = mal.get_resource('anime', role['anime']['mal_id'], use_cached=use_cached)
        anime_db = get_anime_db( anime, use_cached)

        for studio in anime['studios']:
            studio_db = get_studio_db(studio, anime_db, use_cached)

        status.update_status(("updating voice acting roles", f"{role['character']['name']} from {anime['title']}"))

        
        character = mal.get_resource('characters', role['character']['mal_id'], use_cached=use_cached)
         # cos it happend that the character was removed(?) from MAL, so even on MAL on person credits it 
         # appeard it didnt have its own page weird, idn if it can happen to other resources
        if not character:
            continue

        character_db = get_character_db(character, anime_db, use_cached)

        voice_actor_db = get_voice_actor_db(anime, person, character, role['role'], anime_db, person_db, character_db, use_cached)

        status.update_status(("updating voice acting roles", f"{role['character']['name']} from {anime['title']}"))

    print("updated voice rolls")
    status.update_status("updating staff credits", add_progress=False)

    for staff_position in person['anime_staff_positions']:
        anime = mal.get_resource('anime', staff_position['anime']['mal_id'], use_cached=use_cached)
        anime_db = get_anime_db(anime, use_cached)

        for studio in anime['studios']:
            studio_db = get_studio_db(studio, anime_db, use_cached)
            

        position = staff_position['position']
        staff_member_db = get_staff_member_db(anime,person, position, person_db, anime_db, use_cached)

        status.update_status(("updating staff credits", f"{position} in {anime['title']}"))

    print("updated staff positions")
    status.update_status("updating published manga", add_progress=False)

    for published_manga in person['published_manga']:
        
        manga = mal.get_resource('manga', published_manga['manga']['mal_id'], use_cached=use_cached)
        manga_db = get_manga_db(manga, use_cached)

        position = published_manga['position']

        manga_author_db = get_manga_author_db(manga, person, position, manga_db, person_db, use_cached)

        status.update_status(("updating published manga", f"{manga['title']}"))



    print("updated all about person")
    update_function_status("finishing", 1, 1, celery_task )
    db.session.commit()

    
def update_studio_page(mal_id:int, use_cached:bool, celery_task:Task):

    update_function_status("updating studio information", 0, 1, celery_task)

    studio = mal.get_resource('studios', mal_id, use_cached=use_cached)
    studio_db = Studio.query.get(mal_id)
    print(f"UPDATING STUDIO -------- {studio_db.name} -----------")

    if not studio_db:
        studio_db = add_studio(studio)
    elif not use_cached:
        update_studio(studio_db, studio)

    total_progress = 1 + len(studio['anime'])
    status = StatusUpdater(total_progress, celery_task)
    status.update_status("updating studio's anime")
    print("updated studio info")

    for anime_info in studio['anime']:
        anime = mal.get_resource('anime', anime_info['mal_id'], use_cached)

        anime_db = get_anime_db(anime, use_cached)
        studio_db.anime.append(anime_db)
        status.update_status(("updating studio's anime", f"{anime['title']}"))

    print("updated all about studio")
    update_function_status("finishing", 1, 1, celery_task )
    db.session.commit()
        


        




          


        

        
        

