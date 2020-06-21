from flask import Flask , render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug import secure_filename
import os
import datetime

#if forgot mysql aclchmey learn from https://www.tutorialspoint.com/flask_framework_online_training/flask_sql_alchemy.asp
#for clear concept
with open('Config.json','r+') as c:
    p=json.load(c)
    param=p['params']

app = Flask(__name__)

app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = param['local_server']
app.config['UPLOAD_FOLDER']=param['uploader']

#IT IS USE TO CONNECT DATaBSE THROUGH MYSQL like in php you do dbcon.php file
#FOR MYSQL THE ABOVE CONNECTIVITY IS DONE BY THIS STATMENT
db = SQLAlchemy(app)
#this made a class of database

class Contacts(db.Model):
    #here contact is table of coding thunder
    " id name phone msg date email"
    #"these are the above varibles from datbase"
    #and use in downlines to get connect to datbase
    #unique that every value to be unique unique default value is false
    #nullab;le means it can be empty
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),  nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    msg = db.Column(db.String(50),  nullable=False)
    #date = db.Column(db.String(12),  nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)


class Post(db.Model):
    #here contact is table of coding thunder
    " id name phone msg date email"
    #"these are the above varibles from datbase"
    #and use in downlines to get connect to datbase
    #unique that every value to be unique unique default value is false
    #nullab;le means it can be empty
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),  nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(50),  nullable=False)
    img_file = db.Column(db.String(50),  nullable=False)
    date = db.Column(db.String(50),  nullable=False)

@app.route("/")
def home():
    post=Post.query.filter_by().all()[0:param['no_of_post']]
    return render_template('index.html',param=param,posts=post)

@app.route("/about")
def about():
    return render_template('about.html',param=param)


@app.route("/signin",methods=['GET','POST'])
def dashboard():

    if ('user' in session and session['user']==param['admin_user']):
        post = Post.query.all()
        return render_template('dashboard.html', param=param, posts=post)

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if name==param['admin_user'] and password==param['admin_password']:
            session['user']=param['admin_user']
            post=Post.query.all()
            return render_template('dashboard.html',param=param,posts=post)

    return render_template('signin.html',param=param)

@app.route("/contactus",methods=['GET','POST'])
def contact():

    if request.method == 'POST' :
        # """Add entry to the database"""
        # here varible=request.form("html action form name="parameter" ')
        name = request.form.get('name')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        email = request.form.get('email')

        # " id name phone msg email"
        entry = Contacts(name=name, phone=phone, msg=message, email=email)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html',param=param)

@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html', param=param, post=post)


#to fetch all post
#post=Post.query.all()
    #for p in post:
     #   title=p.title
      #  slug=p.slug
       # content=p.content
        #return render_template('post.html', param=param, title=title, slug=slug, content=content)



@app.route("/signature")
def madeby():
    return render_template('signature.html',param=param)


@app.route("/edit/<string:post_id>",methods=['GET','POST'])
def edit(post_id):
    if ('user' in session and session['user']==param['admin_user']):
         if request.method == 'POST':
            title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')
            img_file=request.form.get('img')
            date=datetime.datetime.now()

            if post_id == '0':
              entry=Post(title=title,slug=slug,content=content,img_file=img_file,date=date)
              db.session.add(entry)
              db.session.commit()

            else:
               post=Post.query.filter_by(id=post_id).first()
               post.title=title
               post.slug=slug
               post.content=content
               post.img_file=img_file
               post.date=date
               db.session.commit()


    posts = Post.query.filter_by(id=post_id).first()
    return render_template('edit.html', param=param,post=posts,id=post_id)



@app.route("/uploader",methods=['GET','POST'])
def uploader():
    if ('user' in session and session['user'] == param['admin_user']):
        if request.method == 'POST':
            f=request.files['filename']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            return  "Uploaded Succesfully"


@app.route("/logout",methods=['GET','POST'])
def logout():
   session.pop('user')
   return redirect('/signin')


@app.route("/delete/<string:post_id>",methods=['GET','POST'])
def delete(post_id):
    if ('user' in session and session['user']==param['admin_user']):
       post=Post.query.filter_by(id=post_id).first()
       db.session.delete(post)
       db.session.commit()
       return "Deleted succesfully"



app.run(debug=True)
#app.run(debug= True)