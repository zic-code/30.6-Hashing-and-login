from flask import Flask, redirect, render_template,flash, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import Unauthorized
from models import db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm,DeleteForm
app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashing_and_login'   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jisoos_secret_key'


db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('/users/register.html')

@app.route('/register',methods=['GET','POST'])
def register_form(): 
    form = RegisterForm() 
    #if submit is validate
    print(request.method)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        #
        new_user = User.register(username,password)
        new_user.email = email
        new_user.first_name= first_name
        new_user.last_name = last_name

        db.session.add(new_user)
        db.session.commit()

        flash(f"Welcome, {new_user.username}! Your account has been created.", "success")
        session["username"]= new_user.username
        return redirect('/users/<username>')

    return render_template('/users/register_form.html',form = form)

@app.route('/login',methods = ['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

    # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["username"]=user.username # keep logged in
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ["Bad name/password"]
    

    return render_template('/users/login.html',form = form)

@app.route('/logout',methods = ['POST'])
def logout():
    session.pop("username")
    
    return redirect('/')

@app.route('/users/<username>',methods = ['GET'])
def show(username):
    
    username = session.get('username')
    if not username:
        return redirect('/')
    user = User.query.filter_by(username = username).first()
    feedbacks = Feedback.query.all()
    form = DeleteForm()

    return render_template('users/show.html', user= user, feedbacks= feedbacks,form = form)
    
@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):

    if 'username' not in session or session['username'] != username:
        return redirect('/')
    
    user = User.query.filter_by(username = username).first()

    if user: 
        Feedback.query.filter_by(username=username).delete()

        db.session.delete(user)
        db.session.commit()

        session.pop('username')
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback(username):
    if "username" not in session or username != session['username']:
        redirect('/')
    user = User.query.filter_by(username = username).first()
    form = FeedbackForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/create_feedback.html", form=form,user = user) 
       
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/update_feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")

    
   




if __name__ == '__main__':
    app.run(debug=True)

