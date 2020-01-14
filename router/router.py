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
    ta_info = []
    comments = []
    comment_datetime = []
    ratings = [0, [0, 0, 0]]

    for _, val in ta_object.val().items():
        if val.get("comment") != None and val.get("comment_datetime"):
            str_datetime = val["comment_datetime"]
<<<<<<< HEAD
            str_datetime = datetime.fromisoformat(str_datetime).strftime("%m/%d/%Y, %H:%M:%S")
            comments.append(val["comment"], str_datetime)
=======
            str_datetime = datetime.datetime.fromisoformat(str_datetime)
            str_datetime = str_datetime.strftime("%m/%d/%Y, %H:%M:%S")
            comment_datetime.append(str_datetime)
>>>>>>> preparing for big error fix merge
        if val.get("rating") != None:
            ratings[0] += 1
            ratings[1][0] += val["rating"]["clarity"]
            ratings[1][1] += val["rating"]["helpfulness"]
            ratings[1][2] += val["rating"]["availability"]
    
    if ratings[0] > 0:
        ratings[1][0] /= ratings[0]
        ratings[1][1] /= ratings[0]
        ratings[1][2] /= ratings[0]

<<<<<<< HEAD
    ta_info.append((ta_name, comments, ratings[1]))
    print(ta_info)
=======
    ta_info.append((ta_name, comments, comment_datetime, ratings))
    # print("TA INFO")
    # print(ta_info)
>>>>>>> preparing for big error fix merge

    # adding comment to forum
    my_comment = forum()
    if my_comment.validate_on_submit():
        comment_datetime = datetime.datetime.now().isoformat()
        # print(my_comment.comment.data)
        # print(comment_datetime)
        db.child("TA").child(ta_name).push({
            "comment": my_comment.comment.data,
            "comment_datetime": comment_datetime
        })
        # print("pushed comment")
        return redirect('/TA/'+ta_name)
    else:
        print("error, too long")
        
    # addint rating to TA
    my_rating = rating_form()
    if my_rating.validate_on_submit():
        # print([my_rating.clarity.data, my_rating.helpfulness.data, my_rating.availability.data])
        db.child("TA").child(ta_name).push({
            "rating": {
                "clarity": my_rating.clarity.data, 
                "helpfulness": my_rating.helpfulness.data, 
                "availability":my_rating.availability.data
            }
        })
        # print("pushed rating")

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