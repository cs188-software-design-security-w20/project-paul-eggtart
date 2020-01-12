from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template

)

from forms import forum
from forms import slider
from search import searchBar
from load import database

db = database()#define database

router = Blueprint(
    'router',
    __name__,
    template_folder='../templates'
)

@router.route('/TA/<ta_name>', methods=['GET', 'POST'])
def TA(ta_name):
    ta_info = []
    ta = db.child("TA").child(ta_name).get()
    name = ta.key()
    comments = []
    for _, val in ta.val().items():
      comments.append(val['comment'])
    ta_info.append( (name,comments))


    #rating the TA
    form = forum()
    if form.validate_on_submit():
        db.child("TA").child(ta_name).push({"comment": form.comment.data})
        return redirect('/TA/'+ta_name)


    slider2 = slider()
    if slider2.validate_on_submit():
      print(slider2.clarity.data)

    return render_template('ta_page.html',ta_info=ta_info,redirect='/TA/'+ta_name,form=form, ta_jpg= ta_name+".jpg", slider=slider2 )


@router.route('/search', methods=['GET', 'POST'])
def search():
    search = searchBar()
    if search.validate_on_submit():
        return redirect('/TA/'+ search.ta_name.data)
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


