# -*- coding:utf-8 -*-
from flask import Flask,session,make_response,jsonify,url_for,redirect,request,abort,render_template,flash,send_from_directory
from forms import LoginForm,UploadForm,RichTextForm,NewNoteForm,EditNoteForm
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
import os,uuid,click


app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY','aeteadfASDF')
app.config['MAX_CONTENT_LENGTH']=3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path,'uploads')
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','sqlite:///'+os.path.join(app.root_path,'data.db'))
ckeditor = CKEditor(app)
db = SQLAlchemy(app)


user = {'username' : 'hb Zh','bio':'A boy love movies'}
movies = [{'name' : 'The Big Short','year': '2015'},
        {'name':'Too Big Too Fail','year' :'2011'},
	{'name':'L\'Outsider','year':'2018'}]
@app.cli.command()
def initdb():
    db.create_all()
    click.echo ("init db")

class Note(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.Text)

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','human')
    response ='<h1>hello %s </h1>' % name
    if 'logged_in' in session:
        response += '[authenicated]'
    else:
        abort(403)
    return response

@app.route('/foo')
def foo():
    return '<h1>foo</h1><a href="%s">test</a>' % url_for('do_something',next=request.full_path)

@app.route('/bar')
def bar():
    return '<h1>bar</h1><a href="%s">test</a>' % url_for('do_something',next=request.full_path)

@app.route('/upload-image')
def show_images():
    return render_template('uploaded.html')

@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name',name)
    return response 

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome %s' % username)
        return redirect(url_for('index'))
    #return render_template('login.html',form=form)
    return render_template('bootstrap.html',form=form)

def redirect_back(default='hello',**kwargs):
    for target in request.args.get('next'),request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default,**kwargs))

@app.route('/do_something_and_redirect')
def do_something():
    return redirect_back()


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html',user=user,movies=movies)

@app.route('/flash')
def just_flash():
    flash(u'你好，我是闪电')
    return redirect(url_for('index'))

@app.route('/upload',methods=['GET','POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        flash('Upload success')
        session['filenames']=[filename]
        return redirect(url_for('show_images'))

    return render_template('upload.html',form=form)



@app.route('/upload/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'],filename)

@app.route('/ckeditor',methods=['GET','POST'])
def intergrate_ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash('Your post is published')
        return render_template('post.html',title=title,body=body)
    return render_template('ckeditor.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404

@app.route('/new',methods=['GET','POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_note.html',form=form)

@app.route('/read')
def read_note():
    notes = Note.query.all()
    return render_template('read_notes.html',notes=notes)

@app.route('/edit/<int:note_id>',methods=['GET','POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        note.body = form.body.data
        db.session.commit()
        return redirect(url_for('read_note'))
    form.body = note.body
    return render_template('edit_note.html',form=form)
