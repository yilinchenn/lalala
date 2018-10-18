from flask import render_template, url_for, request, redirect, flash, abort, send_from_directory
from werkzeug.utils import secure_filename
import uuid
import os

from app import webapp
from app.models import User, Photo, PhotoType
from app.login import check_session
from app import db
from wand.image import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@webapp.route('/photos/<photo_id>', methods=["GET"])
def display_images(photo_id):
    user = User.query.filter(User.photos.any(Photo.photo_id==photo_id)).first()
    #print("=================================User %s========================" % user.username)
    #cannot display the page if not logged in
    if(check_session(user.username)):
        return render_template("photo_detail.html", photo_id= photo_id, types = PhotoType)
    flash("Error: you are not logged in")
    return redirect(url_for('login'))

@webapp.route('/photo/<photo_id>/<type>', methods=["GET"])
def display_image(photo_id, type):
    user = User.query.filter(User.photos.any(Photo.photo_id==photo_id)).first()
    print("=================================User %s========================" % user.username)
    #cannot display the page if not logged in
    if(check_session(user.username)):
        photo = Photo.query.filter_by(photo_id=photo_id, type=type).first()
        print("==============================DISPLAY======================= %s" % photo.path)
        return send_from_directory(os.path.dirname(photo.path), photo.path.split('/')[-1], as_attachment=True)
    flash("Error: you are not logged in")
    return redirect(url_for('login'))


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
                photos, fname = get_transformations(temp_file_path)

                save_photos(usr, photos, fname)
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

            #file is ok
            filename = secure_filename(file.filename)
            print("=======FOUND FILE======== %s" % filename)

            temp_file_path = save_temp_photo(usr, file)
            photos, fname = get_transformations(temp_file_path)

            save_photos(usr, photos, fname)

            return "upload: " + filename + " successful"
        else:
            return "ERROR: Wrong password"
    return "ERROR: user does not exist"


def save_temp_photo(user, photo):
    #temp path
    rand_str = str(uuid.uuid4())
    new_filename = rand_str + "." + photo.filename.split('.')[-1]
    path = webapp.config['UPLOAD_FOLDER'] + "/" + user.username + "/" + "temp/" + new_filename

    os.makedirs(os.path.dirname(path), exist_ok=True)
    photo.save(path)
    return path




def save_photos(user, photos, fname):
    #TODO photos = [0, 1, 2, 3]
    #same photo_id for all types
    #of the same photo
    db_photos = []
    photo_id = str(uuid.uuid4())
    for index, photo in enumerate(photos):
        #TODO change type to actual type
        type = index
        #new filename = type.[original file type]
        new_file_name = photo_id + "." + fname.split('.')[-1]
        path = webapp.config['UPLOAD_FOLDER'] + "/" + user.username + "/" + str(type) + "/" + new_file_name
        p = Photo(photo_id=photo_id, type=type, path=path)
        db_photos.append(p)
        user.photos.append(p)

    #try to save to file
    try:
        for index, photo in enumerate(photos):
            #print("========================SAVING========================= %s" % db_photos[index].path)
            os.makedirs(os.path.dirname(db_photos[index].path), exist_ok=True)
            photo.save(filename=db_photos[index].path)
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
def get_transformations(fname):
    #print ("!!!!!!!!!!!!!!!!!!!!!!!enter transformation!!!!!!!!!!!!!!!!!!!!!!!!!!")
    img = Image(filename=fname)
    #print ("!!!!!!!!!!!!!!!!!filename=%s!!!!!!!!!!!!!!!!!!!!!!!!!!!"%fname)
    photos = []
    for type in PhotoType:
        i = img.clone()
        if type == PhotoType.THUMBNAIL:
            #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!thumbnail!!!!!!!!!!!!!!!!!!!!")
            height = 200
            width = int (img.width * height / img.height)
            i.resize(width, height)
        elif type == PhotoType.BLACKWHITE:
            i.type = 'bilevel'
        elif type == PhotoType.FLIPPED:
            i.flip()
        photos.append(i)
    #print ("!!!!!!!!!!!!!!!!!!!!!!!finish transform!!!!!!!!!!!!!!!!!!!!!!!!!")
    return photos,fname

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


