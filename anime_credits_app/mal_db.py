import datetime

from flask_sqlalchemy import SQLAlchemy
from celery.app.task import Task

from anime_credits_app import db, adc, log_n_cache
from anime_credits_app.models import Anime, Person, Character, StaffMember, VoiceActor, Studio

mal = adc.mal


def update_function_status(current_task, progress:int, total:int, celery_task : Task) -> dict:
    if celery_task:
        celery_task.update_state(
            state='PROGRESS',
            meta={
                'current': progress,
                'total' : total,
                'status' : current_task
            })

        print({
                'current': progress,
                'total' : total,
                'status' : current_task
            })


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
    #print(f"new anime db created = {anime['title']}")
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
        




def add_studio(studio : dict) -> Studio:
    studio_db = Studio(
        mal_id = studio['mal_id'],
        work_type = studio['type'],
        name = studio['name'],
        url = studio['url']
    )

    db.session.add(studio_db)
    #print(f"added new studio - {studio['name']}")
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

def update_staff_member(staff_member_db : StaffMember, staff_id, anime:dict, person:dict, position):
    staff_member_db.position = position
    staff_member_db.person_id = person['mal_id']
    staff_member_db.anime_id = anime['mal_id']

def add_voice_actor(voice_actor_id : int, anime : dict, person : dict, character : dict, role : dict) -> VoiceActor:

    language = None
    for voice_actor in character['voice_actors']:
        if voice_actor['mal_id'] == person['mal_id']:
            language = voice_actor['language']
            break

    voice_actor_db = VoiceActor(
        id = voice_actor_id,
        role = role['role'],
        language = language,
        anime_id = anime['mal_id'],
        person_id = person['mal_id'],
        character_id = character['mal_id']
    )

    db.session.add(voice_actor_db)
    #print(f"added new voice actor {voice_actor_id}")
    return voice_actor_db

def update_voice_actor(voice_actor_db:VoiceActor, voice_actor_id : int, anime : dict, person : dict, character : dict, role : dict):
    language = None
    for voice_actor in character['voice_actors']:
        if voice_actor['mal_id'] == person['mal_id']:
            language = voice_actor['language']
            break

    voice_actor_db.role = role['role']
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


# ---------------MAIN FUNCTIONS----------------

def update_staff(anime_mal_id:int, use_cached:bool, celery_task : Task = None):
    print("update staff start")
    update_function_status("updating anime info", 0, 1, celery_task)

    anime = mal.get_resource('anime', anime_mal_id, use_cached=use_cached)
    staff = mal.get_resource('staff', anime_mal_id, use_cached=use_cached) 

    

    anime_db = Anime.query.get(anime_mal_id)
    if not anime_db:
        anime_db = add_anime(anime)
    elif not use_cached:
        update_anime(anime_db, anime)
    print("updated anime")

    current_progess = 2
    total_progress = 2 + len(anime['studios']) + len(staff['staff'])
    update_function_status("updating studios", current_progess, total_progress, celery_task )

    for studio in anime['studios']:
        

        studio_db = Studio.query.get(studio['mal_id'])
        if not studio_db:
            studio_db = add_studio(studio)
            studio_db.anime.append(anime_db)
        elif not use_cached:
            update_studio(studio_db, studio)

        current_progess += 1
        update_function_status(f"updating studios\n{studio['name']}", current_progess, total_progress, celery_task )
        
        
    print("updated studios")
    update_function_status("updating staff", current_progess, total_progress, celery_task )

    for staff_member in staff['staff']:
        person = mal.get_resource('people', staff_member['mal_id'], use_cached=use_cached)

        person_db = Person.query.get(staff_member['mal_id'])
        if not person_db:
            person_db = add_person(person)
        elif not use_cached:
            update_person(person_db, person)

        for position in staff_member['positions']:
            staff_id = f"{anime['mal_id']}/{person['mal_id']}/{position}"

            staff_member_db = StaffMember.query.get(staff_id)
            if not staff_member_db:
                staff_member_db = add_staff_member(staff_id, anime, person, position)

                person_db.staff_credits.append(staff_member_db)
                anime_db.staff.append(staff_member_db)
            elif not use_cached:
                update_staff_member(staff_member_db, staff_id, anime, person, position)

        current_progess += 1
        update_function_status(f"updating staff\n{person['name']}", current_progess, total_progress, celery_task )
                
    print("updated staff")
    update_function_status("finishing", 1, 1, celery_task )
    db.session.commit()

def update_person_credits(person_mal_id : int, use_cached:bool, celery_task:Task = None):
    print("update person credits start")
    update_function_status("updating person info", 0, 1, celery_task)

    person = mal.get_resource('people', person_mal_id, use_cached=use_cached)

    person_db = Person.query.get(person_mal_id)
    if not person_db:
        person_db = add_person(person)
    elif not use_cached:
        update_person(person_db, person)

    print("updated person")
    current_progess = 1
    total_progress = 1 + len(person['voice_acting_roles']) * 2 + len(person['anime_staff_positions'])
    update_function_status("updating voice acting roles", current_progess, total_progress, celery_task )

    for role in person['voice_acting_roles']:
        
        anime = mal.get_resource('anime', role['anime']['mal_id'], use_cached=use_cached)
        anime_db = Anime.query.get(anime['mal_id'])
        if not anime_db:
            anime_db = add_anime(anime)
        elif not use_cached:
            update_anime(anime_db, anime)

        current_progess += 1
        role_description = f"updating voice acting roles\n{role['character']['name']} from {anime['title']}"
        update_function_status(role_description, current_progess, total_progress, celery_task )

        character = mal.get_resource('characters', role['character']['mal_id'], use_cached=use_cached)

        character_db = Character.query.get(character['mal_id'])
        if not character_db:
            character_db = add_character(character)
            anime_db.characters.append(character_db)
        elif not use_cached:
            update_character(character_db, character)
        

        voice_actor_id = f"{anime['mal_id']}/{person['mal_id']}/{character['mal_id']}"
        voice_actor_db = VoiceActor.query.get(voice_actor_id)
        if not voice_actor_db:
            voice_actor_db = add_voice_actor(voice_actor_id, anime, person,character, role)
            
            anime_db.voice_actors.append(voice_actor_db)
            person_db.voice_acting_roles.append(voice_actor_db)
            character_db.voice_actors.append(voice_actor_db)
        elif not use_cached:
            update_voice_actor(voice_actor_db,voice_actor_id, anime, person, character, role)

        current_progess += 1
        update_function_status(role_description, current_progess, total_progress, celery_task )

    print("updated voice rolls")
    update_function_status("updating staff credits", current_progess, total_progress, celery_task )

    for staff_position in person['anime_staff_positions']:
        anime = mal.get_resource('anime', staff_position['anime']['mal_id'], use_cached=use_cached)

        anime_db = Anime.query.get(anime['mal_id'])
        if not anime_db:
            anime_db = add_anime(anime)
        elif not use_cached:
            update_anime(anime_db, anime)

        position = staff_position['position']
        staff_id = f"{anime['mal_id']}/{person['mal_id']}/{position}"

        staff_member_db = StaffMember.query.get(staff_id)
        if not staff_member_db:
            staff_member_db = add_staff_member(staff_id, anime, person,position)

            anime_db.staff.append(staff_member_db)
            person_db.staff_credits.append(staff_member_db)   
        elif not use_cached:
            update_staff_member(staff_member_db, staff_id, anime, person, position) 

        current_progess += 1
        update_function_status(f"updating staff credits\n{position} in {anime['title']}", current_progess, total_progress, celery_task )


    print("updated all about person")
    update_function_status("finishing", 1, 1, celery_task )
    db.session.commit()

    
        


        




          


        

        
        

