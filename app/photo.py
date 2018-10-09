from flask import render_template, url_for, request, redirect, flash, abort
import uuid

from app import webapp
from app.models import User, Photo, PhotoType
from app.login import check_session
from app import db

@webapp.route('/test/FileUpload', methods=["GET", "POST"])
def testUpload():
    if(request.method == 'POST'):
        return do_test_upload(request.form)
    else:
        #print("UPLOAD FOLDER: %s" % webapp.config['UPLOAD_FOLDER'])
        return render_template('test_upload.html')


@webapp.route('/upload/<username>', methods=["POST"])
def upload_photo(username):
    if(request.method == 'POST'):
        if (check_session(username)):
            photos = get_transformations()
            usr = User.query.filter_by(username=username).first()
            if (usr):
                save_photos(usr, photos)
                return redirect(url_for('dashboard', username=username))
            else:
                # cannot find user with username stored in session
                # should be impossible
                abort(500)

        flash("ERROR: you are not logged in")
        return redirect(url_for('login'))


def do_test_upload(form):
    username = form.get('userID')
    password = form.get('password')

    #TODO get the files themselves
    photos = get_transformations()

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


# return a list of transformed photos
# 0 = thumbnail
# 1 = orignal
# 2 = whatever
# 3 = llallala
def get_transformations():
    #TODO: yilin implement this function
    return [0,1,2,3]




