from datetime import datetime
from flask_blog import db,loginmanager
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"User('{self.title}',{self.date_posted}')"
class Genre(db.Model):
    __tablename__ = "genre"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False)

class Languages(db.Model):
    __tablename__ = "languages"
    language_id = db.Column(db.Integer, primary_key=True)
    language_code = db.Column(db.String, nullable=False)
    language_name = db.Column(db.String, nullable=False)
    movie = db.relationship("Movies", backref="languages", lazy=True)

class Countries(db.Model):
    __tablename__ = "countries"
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String, nullable=False)

class Movies(db.Model):
    __tablename__="movie"
    movie_id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String, nullable=False)
    budget =db.Column(db.String, nullable=False)
    overview =db.Column(db.String, nullable=True)
    director = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    #release_date = db.Column(db.Date, nullable=True)
    revenue = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.genre_id"), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey("languages.language_id"), nullable=False)
    tagline =db.Column(db.String, nullable=True)
    vote_average = db.Column(db.Integer, nullable=True)
    vote_count = db.Column(db.Integer, nullable=True)
    image=db.Column(db.String, nullable=True)
    language = db.relationship("Languages", backref="language", lazy=True)
    genre = db.relationship("Genre", backref="genre", lazy=True)

class Comments(db.Model):
    __tablename__ = "moviecomments"
    comm_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), nullable=False)
    mcomment = db.Column(db.String, nullable=False)
    mrating = db.Column(db.Integer, nullable=False)
