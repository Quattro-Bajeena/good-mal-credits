from flask_sqlalchemy import SQLAlchemy
import datetime

from anime_credits_app import db
from anime_credits_app import adc
#import anime_credits_app.adc.mal as mal
from anime_credits_app.models import Anime, Person, Character, StaffMember, VoiceActor, Studio

mal = adc.mal




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

def add_staff_member(staff_id, anime, person, position) -> StaffMember:
    
    new_credit = StaffMember(
        id = staff_id,
        position = position,
        person_id = person['mal_id'],
        anime_id = anime['mal_id']
    )
    db.session.add(new_credit)
    #print(f"added new staff member: {staff_id}")
    return new_credit

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



def acquire_staff(anime_mal_id : int):
    
    anime = mal.get_resource('anime', anime_mal_id)
    staff = mal.get_resource('staff', anime_mal_id) 

    anime_db = Anime.query.get(anime_mal_id)

    if not anime_db:
        anime_db = add_anime(anime)

    print("got anime")

    for studio in anime['studios']:

        studio_db = Studio.query.get(studio['mal_id'])
        if not studio_db:
            studio_db = add_studio(studio)

        studio_db.anime.append(anime_db)


    print("got studios")

    for staff_member in staff['staff']:
        person = mal.get_resource('people', staff_member['mal_id'])

        person_db = Person.query.get(staff_member['mal_id'])
        if not person_db:
            person_db = add_person(person)

        for position in staff_member['positions']:
            staff_id = f"{anime['mal_id']}/{person['mal_id']}/{position}"

            if not StaffMember.query.get(staff_id):
                staff_member_db = add_staff_member(staff_id, anime, person, position)

                person_db.staff_credits.append(staff_member_db)
                anime_db.staff.append(staff_member_db)
                
    
    print("got staff")

    db.session.commit()


def acquire_person(person_mal_id : int):

    person = mal.get_resource('people', person_mal_id)

    person_db = Person.query.get(person_mal_id)

    if not person_db:
        person_db = add_person(person)

    print("got person")

    for role in person['voice_acting_roles']:
        
        anime = mal.get_resource('anime', role['anime']['mal_id'])
        anime_db = Anime.query.get(anime['mal_id'])
        if not anime_db:
            anime_db = add_anime(anime)

        character = mal.get_resource('characters', role['character']['mal_id'])
        character_db = Character.query.get(character['mal_id'])
        if not character_db:
            character_db = add_character(character)

        anime_db.characters.append(character_db)


        voice_actor_id = f"{anime['mal_id']}/{person['mal_id']}/{character['mal_id']}"
        if not VoiceActor.query.get(voice_actor_id):
            voice_actor_db = add_voice_actor(voice_actor_id, anime, person,character, role)
            
            anime_db.voice_actors.append(voice_actor_db)
            person_db.voice_acting_roles.append(voice_actor_db)
            character_db.voice_actors.append(voice_actor_db)

    print("voice rolls")

    for staff_position in person['anime_staff_positions']:
        anime = mal.get_resource('anime', staff_position['anime']['mal_id'])

        anime_db = Anime.query.get(anime['mal_id'])
        if not anime_db:
            anime_db = add_anime(anime)

        position = staff_position['position']
        staff_id = f"{anime['mal_id']}/{person['mal_id']}/{position}"
        if not StaffMember.query.get(staff_id):
            staff_member_db = add_staff_member(staff_id, anime, person,position)

            anime_db.staff.append(staff_member_db)
            person_db.staff_credits.append(staff_member_db)    


    print("got all about person")
    db.session.commit()

    
        


        




          


        

        
        

