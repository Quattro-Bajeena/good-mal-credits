import time, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from anime_credits_app.models import Anime




def not_optimized():
    t1 = time.time()
    print("START")
    anime = Anime.query.get(30)
    print(anime)

    for studio in anime.studios:
        print(studio)

    print("staff----------")
    for member in anime.staff:
        print(member.person.name)
        print(member.position)
        print(member.person.member_favorites)
        print(member.person.birthday)
        print(member.person.birthday)
        print(len(member.person.staff_credits))

    print("roles--------------")
    for role in anime.voice_actors:
        print(role.character.name)
        print(role.character.member_favorites)
        print(role.role)
        print(role.character.image_url)
        print(role.person.image_url)
        print(role.person.mal_id)
        print(role.person.name)
        print(role.person.member_favorites)
        print(role.person.birthday)
        print(role.person.birthday)
        print(role.language)
        print(len(role.person.voice_acting_roles))


    print("TIME: ", time.time() - t1)


def optimized():
    t1 = time.time()
    print("START")
    anime = Anime.query.get(30)
    print(anime)
    studios = anime.studios
    for studio in studios:
        print(studio)

    print("staff----------")
    staff = anime.staff
    for member in staff:
        person = member.person
        print(person.name)
        print(member.position)
        print(person.member_favorites)
        print(person.birthday)
        print(person.birthday)
        print(len(person.staff_credits))

    print("roles--------------")
    roles = anime.voice_actors
    for role in roles:
        character = role.character
        person = role.person

        print(character.name)
        print(character.member_favorites)
        print(role.role)
        print(character.image_url)
        print(person.image_url)
        print(person.mal_id)
        print(person.name)
        print(person.member_favorites)
        print(person.birthday)
        print(person.birthday)
        print(role.language)
        print(len(person.voice_acting_roles))


    print("TIME: ", time.time() - t1)



not_optimized()
#optimized()