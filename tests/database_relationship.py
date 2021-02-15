import time, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from anime_credits_app.models import Anime

t1 = time.time()
print("START")
anime = Anime.query.get(30)
print(anime)
print()
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

