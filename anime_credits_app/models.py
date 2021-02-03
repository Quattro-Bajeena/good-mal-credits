from anime_credits_app import db

# for many-to-many relationship of anime and characters
characters = db.Table('characters',
    db.Column('character_id', db.Integer, db.ForeignKey('character.mal_id'), primary_key=True),
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.mal_id'), primary_key=True)
)

studios = db.Table('studios',
    db.Column('studio_id', db.Integer, db.ForeignKey('studio.mal_id'), primary_key=True),
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.mal_id'), primary_key=True)
)


class Anime(db.Model):
    mal_id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    title = db.Column(db.String(200), nullable=False)
    title_english = db.Column(db.String(200))
    title_japanese = db.Column(db.String(200))
    format_type = db.Column(db.String(50))
    source = db.Column(db.String(50))
    episodes = db.Column(db.Integer)
    status = db.Column(db.String(50))
    aired_from = db.Column(db.DateTime)
    aired_to = db.Column(db.DateTime)
    score = db.Column(db.Float)
    scored_by = db. Column(db.Integer)
    rank = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    members = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    premiered = db.Column(db.String(200))

    staff = db.relationship('StaffMember', backref='anime', lazy=True)
    voice_actors = db.relationship('VoiceActor', backref='anime', lazy=True)
    characters = db.relationship('Character', secondary=characters, lazy='subquery', backref=db.backref('anime', lazy=True))
    

    def __repr__(self):
        return f"Anime: {self.title} - {self.mal_id}"


class Person(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    given_name = db.Column(db.String(200))
    family_name = db.Column(db.String(200))
    birthday = db.Column(db.DateTime)
    member_favorites = db.Column(db.Integer)

    staff_credits = db.relationship('StaffMember', backref='person', lazy=True)
    voice_acting_roles = db.relationship('VoiceActor', backref='person', lazy=True)


    def __repr__(self):
        return f"Person: {self.name} - {self.mal_id}"


  
class Character(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    member_favorites = db.Column(db.Integer)

    voice_actors = db.relationship('VoiceActor', backref='character', lazy=True)

    def __repr__(self):
        return f"{self.name} - {self.mal_id}"


class StaffMember(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    position = db.Column(db.String(200), nullable=False)

    person_id = db.Column(db.Integer, db.ForeignKey('person.mal_id'))
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.mal_id'))
    
    def __repr__(self):
        return f"StaffMember: {self.person_id} / anime: {self.anime_id} / {self.position}"



class VoiceActor(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100))
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.mal_id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.mal_id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.mal_id'))

    def __repr__(self):
        return f"VoiceActor {self.role} - anime: {self.anime_id}"


class Studio(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    # just type in MAL api
    work_type = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))

    
    anime = db.relationship('Anime', secondary=studios, lazy='subquery', backref=db.backref('studios', lazy=True))
    
    
    
class PageStatus(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    last_modified = db.Column(db.DateTime)

    creating = db.Column(db.Boolean)
    updating = db.Column(db.Boolean)
    
    task_id = db.Column(db.String(100))


