from anime_credits_app import app, db
from anime_credits_app.models import Anime, Person, Character, StaffMember, VoiceActor, Studio
from anime_credits_app.mal_db import update_staff

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Anime' : Anime, 'Person' : Person, 
	'Character' : Character,
	 'StaffMember' : StaffMember, 'VoiceActor' : VoiceActor, "Studio" : Studio,
	 'update_staff' : update_staff}


if __name__ == '__main__':
	app.run()
