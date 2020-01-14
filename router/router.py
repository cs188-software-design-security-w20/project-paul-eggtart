from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template
)
from custom_wtforms.forum_forms import comment_form, rating_form
from search import searchBar
from load import database
from forms import forum
import datetime

db = database() #define database


router = Blueprint(
    'router',
    __name__,
    template_folder='../templates'
)


@router.route('/TA/<ta_name>', methods=['GET', 'POST'])
def TA(ta_name):
    ta_info = []
    ta = db.child("TA").child(ta_name).get()
    data = []
    for _, val in ta.val().items():
        if val.get("comment")!= None: #comment
            data.append( (val["comment"],val["timestamp"].split(" ")[0]))

        elif val.get("rating")!= None: # rating
            print(val["rating"])

    ta_info= (ta_name,data) 

    # adding comment to forum
    my_comment = forum()
    if my_comment.validate_on_submit():

        db.child("TA").child(ta_name).push({"comment": my_comment.comment.data,
                                        "timestamp": str(datetime.datetime.now()) })
        return redirect('/TA/'+ta_name)
    else:
        print("error, too long")
        
    # addint rating to TA
    my_rating = rating_form()
    if my_rating.validate_on_submit():
        print(my_rating.clarity.data)
        print(my_rating.helpfulness.data)
        print(my_rating.availability.data)
        db.child("Ratings").child(ta_name).push({"rating": [my_rating.clarity.data, my_rating.helpfulness.data, my_rating.availability.data]})

    return render_template('ta_page.html', ta_info=ta_info, redirect='/TA/'+ta_name, 
        comment_form=my_comment, rating_form=my_rating, ta_jpg= ta_name+".jpg")



@router.route('/search', methods=['GET', 'POST'])
def search():
    search = searchBar()
    if search.validate_on_submit():
        return redirect('/TA/'+search.ta_name.data)
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