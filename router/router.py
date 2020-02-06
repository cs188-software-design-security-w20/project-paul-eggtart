# organizational purposes
import sys
sys.path.append('./router_logic')

# imports
from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    Flask,
    escape,
    flash
)
from forum_forms import comment_form, rating_form
from TA_functions import *
from signup_db import SignUpForm
from login_db import LoginForm
from email_db import EmailForm
from search import searchBar, closest_match
from profile.profile import User
from load import database
import datetime

# define the database
db = database()

router = Blueprint(
    'router',
    __name__,
    template_folder='../templates'
)


@router.route('/TA/<ta_name>', methods=['GET', 'POST'])
def TA(ta_name):
    ta_object = db.child("TA").child(ta_name).get()

    # get the TA information to display
    comments = parse_ta_comments(ta_object)
    ratings = parse_ta_ratings(ta_object)
    classes = get_ta_classes(ta_object)
    print(ta_name)
    display_name = name_to_string(ta_name)
    print(display_name)
    ta_info = (display_name, comments, ratings, classes)

    # adding comment to forum
    my_comment = comment_form()
    if my_comment.validate_on_submit():
        submit_comment(db, ta_name, my_comment)
        return redirect('/TA/'+ta_name)
    else:
        print("comment validate on submit failed...")

    # addint rating to TA
    my_rating = rating_form()
    if my_rating.validate_on_submit():
        submit_rating(db, ta_name, my_rating)
        return redirect('/TA/'+ta_name)
    else:
        print("rating validate on submit failed...")

    # redner the template
    return render_template('ta_page.html', ta_info=ta_info, redirect='/TA/'+ta_name,
        comment_form=my_comment, rating_form=my_rating, ta_jpg= ta_name+".jpg")



@router.route('/search', methods=['GET', 'POST'])
def search():
    search = searchBar()
    if search.validate_on_submit():
        correction = closest_match(search.ta_name.data)
        name = correction[0][0]
        score = correction[0][1]
        if(score < 90):
            print("not_found")
            return render_template('search.html', form=search)
        return redirect('/TA/'+ name)
    return render_template('search.html', form=search)



@router.route('/')
def home():
    return render_template('index.html')



@router.route('/login', methods=['GET'])
def login():
    username = "Nick"
    context = {
        "data": username
    }
    return render_template('login.html', **context)

@router.route('/profile', methods=['GET'])
def profile():
    context = {
        "user": User().get_user(db, 1)
    }
    return render_template('profile.html', **context)

@router.route('/profile/edit', methods=['GET'])
#@login_required
def profile_edit():
    id = request.args.get('id', None)
    parameters = User().get_parameters()
    context = {
        "parameters": parameters,
        "user": User().get_user(db, id)
    }
    return render_template('profile_edit.html', **context)

@router.route('/profile/edit', methods=['POST'])
#@login_required
def profile_edit_add():
    status = User().update_user(request.form)
    if status == "Success":
        return redirect('/profile')
    else:
        id = request.form.get('id', None)
        context = {
            "parameters": User().get_parameters(),
            "user": User().get_user(db, id)
        }
        return render_template('profile_edit.html', **context)

@router.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = EmailForm()
    if form.validate_on_submit():
        found = False
        users = db.child("users").get().val()
        print(users)
        for u in users:
            data = users[u]
            if data['email'] == form.email.data:
                found = True
                if data['authenticated'] is True:
                    send_password_reset_email(form.email.data)
                    flash('Please check your email for a password reset link.', 'success')
                else:
                    flash('Your email address must be confirmed before attempting a password reset.', 'error')
                    return redirect(url_for('users.login'))
                break
        if found is False:
            flash('Invalid email address!', 'error')
            return render_template('password_reset_email.html', form=form)
    return render_template('password_reset_email.html', form=form)

