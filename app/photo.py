from flask import render_template, url_for, request, redirect, flash, abort
from werkzeug.utils import secure_filename
import uuid
import os

from app import webapp
from app.models import User, Photo, PhotoType
from app.login import check_session
from app import db

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


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

            if 'uploadedfile' not in request.files:
                flash('Error: No file part')
                return redirect(url_for('dashboard', username=username))
            file = request.files['uploadedfile']
            if file.filename == '':
                flash('Error: No selected file')
                return redirect(url_for('dashboard', username=username))
            if file and not allowed_file(file.filename):
                #filename = secure_filename(file.filename)
                flash('Error: file type not allowed')
                return redirect(url_for('dashboard', username=username))

            #file is ok
            filename = secure_filename(file.filename)
            print("=======FOUND FILE======== %s" % filename)



            usr = User.query.filter_by(username=username).first()
            if (usr):

                temp_file_path = save_temp_photo(usr, file)
                photos = get_transformations(temp_file_path)

                #save_photos(usr, photos)
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

    usr = User.query.filter_by(username=username).first()
    if(usr):
        if (usr.check_password(password)):

            if 'uploadedfile' not in request.files:
                return 'Error: No file part'
            file = request.files['uploadedfile']
            if file.filename == '':
                return 'Error: No selected file'
            if file and not allowed_file(file.filename):
                #filename = secure_filename(file.filename)
                return 'Error: file type not allowed'

            temp_file_path = save_temp_photo(usr, file)


            # TODO get the files themselves
            photos = get_transformations(temp_file_path)

            #save_photos(usr, photos)
            return '.'.join(str(e) for e in photos)
        else:
            return "ERROR: Wrong password"
    return "ERROR: user does not exist"


def save_temp_photo(user, photo):
    #temp path
    path = webapp.config['UPLOAD_FOLDER'] + "/" + user.username + "/" + "temp/" + photo.filename

    os.makedirs(os.path.dirname(path), exist_ok=True)
    photo.save(path)
    return path




def save_photos(user, photos):
    #TODO photos = [0, 1, 2, 3]
    #same photo_id for all types
    #of the same photo
    db_photos = []
    photo_id = str(uuid.uuid4())
    for index, photo in enumerate(photos):
        #TODO change type to actual type
        type = index
        #new filename = type.[original file type]
        new_file_name = photo_id + "." + photo.filename.split('.')[1]
        path = webapp.config['UPLOAD_FOLDER'] + "/" + user.username + "/" + str(type) + "/" + new_file_name
        p = Photo(photo_id=photo_id, type=type, path=path)
        db_photos.append(p)
        user.photos.append(p)

    #try to save to file
    try:
        for index, photo in enumerate(photos):
            print("========================SAVING========================= %s" % db_photos[index].path)
            os.makedirs(os.path.dirname(db_photos[index].path), exist_ok=True)
            photo.save(db_photos[index].path)
    except:
        #if files are not saved then do not save to db
        db.session.rollback()
    finally:
        db.session.commit()
    return




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
def get_transformations(photo):
    #TODO: yilin implement this function
    photos = []
    for type in PhotoType:
        photos.append(photo)
    return photos

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


