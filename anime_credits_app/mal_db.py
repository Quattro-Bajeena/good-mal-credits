from flask_sqlalchemy import SQLAlchemy
import datetime

from anime_credits_app import db
from anime_credits_app import adc
#import anime_credits_app.adc.mal as mal
from anime_credits_app.models import Anime, Person, Character, StaffMember, VoiceActor, Studio

mal = adc.mal

# returns a list of dict with picture, name, postion
def update_staff(anime_mal_id : int):
    
    
    if not bool(Anime.query.get(anime_mal_id)):
        print("anime not in database")

        if not mal.check_file('anime', anime_mal_id):
            anime = mal.get_anime_api(anime_mal_id)
            mal.save_anime(anime)
        else:
            anime = mal.get_data_file('anime', anime_mal_id)

        if not mal.check_file('staff', anime_mal_id):
            staff = mal.get_staff_api(anime_mal_id)
            mal.save_staff(anime_mal_id, staff)
        else:
            staff = mal.get_data_file('staff', anime_mal_id)
        
    

        anime_db = Anime(
            mal_id = anime_mal_id,
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
        print(f"new anime db created = {anime['title']}")
        db.session.add(anime_db)
        
    else:
        print("anime in database")
        anime = mal.get_data_file('anime', anime_mal_id)
        staff = mal.get_data_file('staff', anime_mal_id)
        anime_db = Anime.query.get(anime_mal_id)

    print("got anime")

    for studio in anime['studios']:
        if not bool(Studio.query.get(studio['mal_id'])):
            print("studio not in database")
            studio_db = Studio(
                mal_id = studio['mal_id'],
                work_type = studio['type'],
                name = studio['name'],
                url = studio['url']
            )

            studio_db.anime.append(anime_db)
            db.session.add(studio_db)
            print(f"added new studio - {studio['name']}")

        else:
            print("studio in database")
            studio_db = Studio.query.get(studio['mal_id'])
            studio_db.anime.append(anime_db)


    print("got studios")

    for staff_member in staff['staff']:
        if not Person.query.get(staff_member['mal_id']):
            

            if not mal.check_file('people', staff_member['mal_id']):
                print("person doesnt exists - downloading")
                person = mal.get_person_api(staff_member['mal_id'])
                mal.save_person(person)
            else:
                print("person doesnt exists - file already exists")
                person = mal.get_data_file('people', staff_member['mal_id'])
           
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
            print(f"added new person - {person['name']}")
            
        else:
            print("person alraedy exists")
            person_db = Person.query.get(staff_member['mal_id'])
            person = mal.get_data_file('people', staff_member['mal_id'])

        for position in staff_member['positions']:
            
            staff_id = f"{anime['mal_id']}/{person['mal_id']}/{position}"
            if not StaffMember.query.get(staff_id):
                new_credit = StaffMember(
                    id = staff_id,
                    position = position,
                    person_id = person['mal_id'],
                    anime_id = anime['mal_id']
                )
                db.session.add(new_credit)
                person_db.staff_credits.append(new_credit)
                anime_db.staff.append(new_credit)
                print(f"added new staff credit - {staff_id}")
    
    print("got staff")

    db.session.commit()



          


        

        
        

