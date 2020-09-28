import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort,jsonify
from flask_blog import app,db,bcrypt
from flask_blog.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from flask_blog.models import User,Post,Genre,Languages,Countries,Movies,Comments
from flask_login import login_user,current_user,logout_user,login_required
#from models import *
from werkzeug.utils import secure_filename


#@app.route("/")
@app.route("/hello")
def hello():
    posts=Post.query.all()
    return render_template('home.html',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',title=about)


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hello'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html',title='login',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/img',picture_fn)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='img/'+current_user.image_file)
    return render_template('account.html',title='Account',
                    image_file=image_file,form=form)

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is submitted','success')
        return redirect(url_for('hello'))
    return render_template('create_post.html',title='New Post',form=form,legend='Update Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)







@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updates','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content

    return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')
@app.route("/")
def index():
    genreList=Genre.query.order_by("genre_name").all()
    langList=Languages.query.all()
    movList= Movies.query.all()
    return render_template("addMovie.html",genlist=genreList, langlist=langList, movList=movList)

@app.route("/layout")
def dashboard():
    return render_template("layout.html")

@app.route("/addgenre")
def addgenre():
    return render_template("addgenre.html")


@app.route("/genre", methods=["POST"])
def genre():
    """Add a genre."""

    # Get form information.
    name = request.form.get("name")
    genre = Genre(genre_name=name)
    db.session.add(genre)
    db.session.commit()
    return render_template("layout.html")


@app.route("/addlanguage")
def addlanguage():
    return render_template("addlanguage.html")


@app.route("/language", methods=["POST"])
def language():
    """Add a language."""
    # Get form information.
    name = request.form.get("name")
    code = request.form.get("code")
    language = Languages(language_code=code,language_name=name)
    db.session.add(language)
    db.session.commit()
    return render_template("layout.html")

@app.route("/addMovie")
def addMovie():
    genreList=Genre.query.all()
    langList=Languages.query.all()
    cntList= Countries.query.all()
    return render_template("addMovie.html", genlist=genreList, langlist=langList,cntList=cntList)

@app.route("/movie", methods=["POST"])
def movie():
    title =request.form.get("title")
    budget =request.form.get("budget")
    overview =request.form.get("overview")
    director = request.form.get("director")
    country= request.form.get("country")
    release_date = request.form.get("release_date")
    revenue = request.form.get("revenue")
    duration = request.form.get("duration")
    genre_id = request.form.get("genre_id")
    language_id = request.form.get("language_id")
    tagline =request.form.get("tagline")
    f = request.files['file']
    movie = Movies(title=title, budget=budget, overview=overview,director=director,country=country, revenue=revenue, duration=duration,genre_id=genre_id,language_id=language_id,vote_average=0.0, vote_count=0,tagline=tagline,image=f.filename)
    db.session.add(movie)
    db.session.commit()
    f.save(secure_filename(f.filename))
    return render_template("layout.html")

@app.route("/comments/<int:mid>")
def comments(mid):
    movList=Movies.query.filter_by(movie_id=mid).all()
    comList=Comments.query.filter_by(movie_id=mid).all()
    return render_template("comments.html", movList=movList, comList=comList)


@app.route("/saveComment/<int:mid>",methods=["POST"])
def saveComment(mid):
    ratg =request.form.get("rating")
    comm =request.form.get("comment")
    comnt = Comments(movie_id=mid, mrating=ratg, mcomment=comm)
    db.session.add(comnt)
    db.session.query(Movies).filter(Movies.movie_id==mid).update({Movies.vote_average:(Movies.vote_average+ratg)/(Movies.vote_count+1),Movies.vote_count:Movies.vote_count+1}, synchronize_session = False)
    db.session.commit()
    movList=Movies.query.filter_by(movie_id=mid).all()
    comList=Comments.query.filter_by(movie_id=mid).all()
    return render_template("comments.html", movList=movList, comList=comList)
