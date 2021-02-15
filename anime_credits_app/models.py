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

    staff = db.relationship('StaffMember', lazy=True, backref=db.backref('anime', lazy=True) )
    voice_actors = db.relationship('VoiceActor',lazy=True, backref= db.backref('anime', lazy=True) )
    characters = db.relationship('Character', secondary=characters, lazy=True, backref=db.backref('anime', lazy=True))
    

    def __repr__(self):
        return f"Anime: {self.title} - {self.mal_id}"


class Manga(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))

    title = db.Column(db.String(200), nullable=False)
    title_english = db.Column(db.String(200))
    title_japanese = db.Column(db.String(200))

    image_url = db.Column(db.String(200))
    status = db.Column(db.String(50))
    work_type = db.Column(db.String(50))

    volumes = db.Column(db.Integer)
    chapters = db.Column(db.Integer)

    publishing = db.Column(db.String(50))
    published_from = db.Column(db.DateTime)
    published_to = db.Column(db.DateTime)

    rank = db.Column(db.Integer)
    score = db.Column(db.Float)
    scored_by = db. Column(db.Integer)
    
    popularity = db.Column(db.Integer)
    members = db.Column(db.Integer)
    favorites = db.Column(db.Integer)

    serialization = db.Column(db.String(100))

    authors = db.relationship('MangaAuthor', lazy=True, backref=db.backref('manga', lazy=True) )


class Person(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    given_name = db.Column(db.String(200))
    family_name = db.Column(db.String(200))
    birthday = db.Column(db.DateTime)
    member_favorites = db.Column(db.Integer)

    staff_credits = db.relationship('StaffMember', lazy=True, backref=db.backref('person', lazy=True) )
    voice_acting_roles = db.relationship('VoiceActor', lazy=True, backref=db.backref('person', lazy=True) )
    published_manga = db.relationship('MangaAuthor', lazy=True, backref=db.backref('person', lazy=True) )


    def __repr__(self):
        return f"Person: {self.name} - {self.mal_id}"


class Character(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    member_favorites = db.Column(db.Integer)

    voice_actors = db.relationship('VoiceActor', lazy=True, backref=db.backref('character', lazy=True) )

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


class MangaAuthor(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    position = db.Column(db.String(100))
    author_type = db.Column(db.String(100))
    person_id = db.Column(db.Integer, db.ForeignKey('person.mal_id'))
    manga_id = db.Column(db.Integer, db.ForeignKey('manga.mal_id'))

    def __repr__(self):
        return f"MangaAuthor pos:{self.position}, person:{self.person_id}, manga:{self.manga_id}"

class Studio(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    # just type in MAL api
    work_type = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))

    
    anime = db.relationship('Anime', secondary=studios, lazy=True, backref=db.backref('studios', lazy=True))

    def __repr__(self):
        return f"Studio {self.name}"
    
    
    
class PageStatus(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    
    mal_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    exists = db.Column(db.Boolean, default=False, nullable=False)

    last_modified = db.Column(db.DateTime)
    updating = db.Column(db.Boolean, default=False)
    scheduled_to_update = db.Column(db.Boolean, default=False)
    
    task_id = db.Column(db.String(100))

    def __repr__(self):
        return f"PageStatus {self.id}, exists: {self.exists}, updating:{self.updating}, last modified: {self.last_modified}"



category_models = {
    'anime' : Anime,
    'people' : Person,
    'studios' : Studio
}


