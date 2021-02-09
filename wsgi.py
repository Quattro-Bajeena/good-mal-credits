from anime_credits_app import app, db, celery
from anime_credits_app.models import Anime, Person, Character, StaffMember, VoiceActor, Studio
from anime_credits_app.mal_db import update_characters_staff, update_person_credits


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Anime' : Anime, 'Person' : Person, 
	'Character' : Character,
	 'StaffMember' : StaffMember, 'VoiceActor' : VoiceActor, "Studio" : Studio,
	 'update_characters_staff' : update_characters_staff, 'update_person_credits' : update_person_credits,
	 'celery' : celery}


if __name__ == '__main__':
	app.run()
