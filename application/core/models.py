"""Data models."""
from application import db


class User(db.Model):
    """Data model for user accounts."""
    __tablename__ = 'Psychomusic-users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Track(db.Model):
    """Data model for spotify track."""
    __tablename__ = 'Psychomusic-tracks'
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.String(64), index=True, unique=True, nullable=False)
    name = db.Column(db.String(100), index=False, unique=False, nullable=False)
    danceability = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    loudness = db.Column(db.Float, nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    acousticness = db.Column(db.Float, nullable=False)
    instrumentalness = db.Column(db.Float, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    valence = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Integer, nullable=False)
    mood_label = db.Column(db.String(40))

    def __repr__(self):
        return '<Track {} - {}>'.format(self.name, self.track_id)

    def get_json(self):
        data = self.__dict__
        del data['_sa_instance_state']
        return data
    pass