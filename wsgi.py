from anime_credits_app import app, db
from anime_credits_app.models import Anime, Person, Character, StaffMember, VoiceActor, Studio
from anime_credits_app.mal_db import acquire_staff, acquire_person

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Anime' : Anime, 'Person' : Person, 
	'Character' : Character,
	 'StaffMember' : StaffMember, 'VoiceActor' : VoiceActor, "Studio" : Studio,
	 'acquire_staff' : acquire_staff, 'acquire_person' : acquire_person}


if __name__ == '__main__':
	app.run()
