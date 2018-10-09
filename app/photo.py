from flask import render_template, url_for, request, redirect
import uuid
from enum import Enum

from app import webapp
from app.models import User
from app.models import Photo
from app import db

@webapp.route('/test/FileUpload', methods=["GET", "POST"])
def testUpload():
    if(request.method == 'POST'):
        return do_test_upload(request.form)
    else:
        return render_template('test_upload.html')

def do_test_upload(form):
    username = form.get('userID')
    password = form.get('password')

    #TODO get the files themselves
    photos = get_tranformed_photos()

    usr = User.query.filter_by(username=username).first()
    if(usr):
        if (usr.check_password(password)):
            save_photos(usr, photos)
            return '.'.join(str(e) for e in photos)
        else:
            return "ERROR: Wrong password"
    return "ERROR: user does not exist"


def save_photos(user, photos):
    #TODO photos = [0, 1, 2, 3]
    #same photo_id for all types
    #of the same photo
    photo_id = str(uuid.uuid4())
    for photo in photos:
        #TODO change type to actual type
        type = photo
        path = assemble_path(user.username, photo_id, type)
        p = Photo(photo_id=photo_id, type=type, path=path)
        user.photos.append(p)
    db.session.commit()

def assemble_path(first, second, third):
    return "/" + str(first) + "/" + str(second) + "/" + str(third) + ".jpg"



# return a list of transformed photos
# 0 = thumbnail
# 1 = orignal
# 2 = whatever
# 3 = llallala
def get_tranformed_photos():
    #TODO: yilin implement this function
    return [0,1,2,3]


def get_thumbs(username):
    usr = User.query.filter_by(username=username).first()
    #print(usr)
    photos = usr.photos
    #print(photos)
    thumbnails = []

    for photo in photos:
        if photo.type == PhotoType.THUMBNAIL.value:
            #print("=========================================")
            #print(photo)
            thumbnails.append(photo)
    return thumbnails


def get_transformations():
    #TODO implement
    return None


class PhotoType(Enum):
    THUMBNAIL = 0
    ORIGINAL = 1
    BLACKWHITE = 2
    SEPIA = 3



