from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template
)
from forum_forms import comment_form, rating_form
from load import database
import datetime



def parse_ta_comments(ta_object):
    comments = []

    for _, val in ta_object.val().items():
        if val.get("comment") != None and val.get("comment_datetime") != None:
            str_datetime = val["comment_datetime"]
            str_datetime = datetime.datetime.fromisoformat(str_datetime).strftime("%m/%d/%Y, %H:%M:%S")
            comments.append((val["comment"], str_datetime))
    
    return comments



def parse_ta_ratings(ta_object):
    ratings = [0, [0, 0, 0]]

    for _, val in ta_object.val().items():
        if val.get("rating") != None:
            ratings[0] += 1
            ratings[1][0] += val["rating"]["clarity"]
            ratings[1][1] += val["rating"]["helpfulness"]
            ratings[1][2] += val["rating"]["availability"]

    if ratings[0] > 0:
        ratings[1][0] = str(round(ratings[1][0] / ratings[0], 2))
        ratings[1][1] = str(round(ratings[1][1] / ratings[0], 2))
        ratings[1][2] = str(round(ratings[1][2] / ratings[0], 2))

    return ratings[1]



def submit_comment(db, ta_name, my_comment):
    comment_datetime = datetime.datetime.now().isoformat()
    # print(my_comment.comment.data)
    # print(comment_datetime)
    db.child("TA").child(ta_name).push({
        "comment": my_comment.comment.data,
        "comment_datetime": comment_datetime
    })
    # print("pushed comment")



def submit_rating(db, ta_name, my_rating):
    # print([my_rating.clarity.data, my_rating.helpfulness.data, my_rating.availability.data])
    db.child("TA").child(ta_name).push({
        "rating": {
            "clarity": my_rating.clarity.data, 
            "helpfulness": my_rating.helpfulness.data, 
            "availability":my_rating.availability.data
        }
    })
    # print("pushed rating")