from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import os
import time
import pymysql
import config

app = Flask(__name__)
app.secret_key = "tourism_secret"

# Upload settings for admin image uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Return True if the filename has an allowed image extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


db = pymysql.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

# Context processor to pass states and places to all templates
@app.context_processor
def inject_states():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM states")
    states = cursor.fetchall()
    
    # Get places for each state
    states_with_places = []
    for state in states:
        cursor.execute("SELECT * FROM places WHERE state_id=%s", (state['id'],))
        places = cursor.fetchall()
        state['places'] = places
        states_with_places.append(state)
    
    return {'all_states': states_with_places}

# HOME PAGE

@app.route('/')
def home():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM states")

    states = cursor.fetchall()

    return render_template("index.html", states=states)


# STATES PAGE

@app.route('/states')
def states():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM states")

    states = cursor.fetchall()

    return render_template("states.html", states=states)


# PLACES PAGE

@app.route('/places/<int:state_id>')
def places(state_id):

    cursor = db.cursor()

    # Get state information
    cursor.execute("SELECT * FROM states WHERE id=%s", (state_id,))
    state = cursor.fetchone()

    cursor.execute(
    "SELECT * FROM places WHERE state_id=%s",
    (state_id,)
    )

    places = cursor.fetchall()

    return render_template("places.html", places=places, state=state)


# GALLERY PAGE

@app.route('/place/<int:place_id>')
def gallery(place_id):

    cursor = db.cursor()

    cursor.execute(
    "SELECT * FROM places WHERE id=%s",
    (place_id,)
    )

    place = cursor.fetchone()

    cursor.execute(
    "SELECT * FROM place_images WHERE place_id=%s",
    (place_id,)
    )

    images = cursor.fetchall()

    return render_template(
    "gallery.html",
    place=place,
    images=images
    )


# CONTACT PAGE

@app.route('/contact', methods=['GET','POST'])
def contact():

    if request.method == "POST":

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        cursor = db.cursor()

        cursor.execute(
        "INSERT INTO contact_messages(name,email,message) VALUES(%s,%s,%s)",
        (name,email,message)
        )

        db.commit()

    return render_template("contact.html")


# LOGIN PAGE

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email,password)
        )

        user = cursor.fetchone()

        if user:

            session['role'] = user['role']

            if user['role'] == "admin":
                return redirect('/admin/dashboard')

            return redirect('/')

    return render_template("login.html")


# ADMIN DASHBOARD

@app.route('/admin/dashboard')
def dashboard():

    if session.get("role") != "admin":
        return redirect('/login')

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM states")
    states = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM places")
    places = cursor.fetchone()

    return render_template(
        "admin/dashboard.html",
        states=states,
        places=places
    )


# ADD PLACE

@app.route('/admin/add_place', methods=['GET','POST'])
def add_place():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM states")
    states = cursor.fetchall()

    if request.method == "POST":

        place = request.form['place']
        state = request.form['state']
        desc = request.form['description']
        image = request.form['image']

        cursor2 = db.cursor()

        cursor2.execute(
        "INSERT INTO places(place_name,state_id,description,image) VALUES(%s,%s,%s,%s)",
        (place,state,desc,image)
        )

        db.commit()

        return redirect('/admin/dashboard')

    return render_template("admin/add_place.html", states=states)


# ADD GALLERY IMAGE

@app.route('/admin/add_gallery', methods=['GET','POST'])
def add_gallery():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM places")

    places = cursor.fetchall()

    if request.method == "POST":

        place = request.form.get('place')
        image_name = ""

        # Prefer a file upload, fall back to a typed filename
        file = request.files.get('image_file')
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Avoid filename collisions with a timestamp prefix
                filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                image_name = filename
        else:
            image_name = request.form.get('image', '').strip()

        if image_name:
            cursor2 = db.cursor()
            cursor2.execute(
            "INSERT INTO place_images(place_id,image) VALUES(%s,%s)",
            (place,image_name)
            )
            db.commit()
            return redirect('/admin/dashboard')

        # No image provided; show the form again with a simple error message
        return render_template(
            "admin/add_gallery.html",
            places=places,
            error="Please choose an image file to upload or enter an existing filename."
        )

    return render_template("admin/add_gallery.html", places=places)


if __name__ == "__main__":
    app.run(debug=True)