from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange
import wtforms as wtf
from datetime import datetime
from dotenv import load_dotenv
import requests, os

# Get absolute path to /templates and /static
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.abspath(os.path.join(base_dir, '../templates'))
static_dir = os.path.abspath(os.path.join(base_dir, '../static'))

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URI = os.getenv("DATABASE_URI")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, instance_path="/tmp")
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
Bootstrap5(app)

current_year = datetime.now().year

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    title: Mapped[str] = mapped_column(String(250), unique=True) 
    year: Mapped[int] = mapped_column(Integer)
    description : Mapped[str] = mapped_column(String(250))
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(250))
    img_url: Mapped[str] = mapped_column(String(250))

movies = [
    Movie(
        title="The Dark Knight",
        year=2008,
        description="When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and moral tests of his ability to fight injustice.",
        rating=10,
        ranking=1,
        review="Heath Ledger's Joker redefined comic book villains. Dark, intense, and unforgettable.",
        img_url="static/img/the_dark_knight.jpg"
    ),
    Movie(
        title = "Inception",
        year = 2010,
        description = "A skilled thief is given a chance at redemption if he can successfully perform an inception — planting an idea into a target's subconscious.",
        rating=8.5,
        ranking=5,
        review = "Mind-bending and visually stunning. A masterpiece by Nolan.",
        img_url = "static/img/inception.jpg"
    ),
    Movie(
        title="Interstellar",
        year=2014,
        description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        rating=9.2,
        ranking=3,
        review="Emotionally powerful and scientifically ambitious.",
        img_url="static/img/interstellar.jpg"
    ),
    Movie(
        title="The Shawshank Redemption",
        year=1994,
        description="Two imprisoned men bond over years, finding solace and redemption through acts of common decency.",
        rating=9.5,
        ranking=2,
        review="A timeless story of hope and humanity.",
        img_url="static/img/the_shawshank_redemption.jpg"
    ),
    Movie(
        title="The Godfather",
        year=1972,
        description="The aging patriarch of an organized crime dynasty transfers control to his reluctant son.",
        rating=9.0,
        ranking=4,
        review="Flawless acting and storytelling. A cinematic legend.",
        img_url="static/img/the_godfather.jpg"
    )
]

with app.app_context():
    db.create_all()

    for movie in movies:
        db.session.add(movie)
    db.session.commit()

# Edit Form
class MovieForm(FlaskForm):
    title = wtf.StringField("Movie Title", validators=[DataRequired()])
    year = wtf.IntegerField("Release Year", validators=[DataRequired(), NumberRange(min=1888, max=current_year)])
    description = wtf.TextAreaField("Description", validators=[DataRequired(), Length(max=250)])
    rating = wtf.FloatField("Rating", validators=[InputRequired(), NumberRange(min=0.0, max=10,)])
    ranking = wtf.IntegerField("Ranking", validators=[DataRequired(), NumberRange(min=1)])
    review = wtf.TextAreaField("Review", validators=[DataRequired(), Length(max=250)])
    img_url = wtf.StringField("Image URL", validators=[DataRequired()])
    submit = wtf.SubmitField("Save")

class AddMovieForm(FlaskForm):
    title = wtf.StringField("Movie Title", validators=[DataRequired()])
    submit = wtf.SubmitField("Save")

@app.route("/")
def home():
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars()
    return render_template("index.html", movies=all_movies)


@app.route("/edit/<int:movie_id>", methods=['GET', 'POST'])
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    form = MovieForm(obj=movie)
    if request.method == "POST":
        if form.validate_on_submit():
            movie.title = form.title.data
            movie.year = form.year.data
            movie.description = form.description.data
            movie.rating = form.rating.data
            movie.ranking = form.ranking.data
            movie.review = form.review.data
            movie.img_url = form.img_url.data
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete/<int:movie_id>", methods=['GET', 'POST'])
def delete(movie_id):
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddMovieForm()
    if request.method == 'GET':
        return render_template("add.html", form=form)
    if form.validate_on_submit():
        
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
