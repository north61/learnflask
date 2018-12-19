# -*- coding:utf-8 -*-
from flask import Flask,session,make_response,jsonify,url_for,redirect,request,abort,render_template,flash,send_from_directory
from forms import LoginForm,UploadForm
import os,uuid


app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY','aeteadfASDF')
app.config['MAX_CONTENT_LENGTH']=3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path,'uploads')

user = {'username' : 'hb Zh','bio':'A boy love movies'}
movies = [{'name' : 'The Big Short','year': '2015'},
        {'name':'Too Big Too Fail','year' :'2011'},
	{'name':'L\'Outsider','year':'2018'}]

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404

	


