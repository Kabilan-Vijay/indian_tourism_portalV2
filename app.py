from flask import Flask, render_template, request, redirect, session
import pymysql
import config

app = Flask(__name__)
app.secret_key = "tourism_secret"

db = pymysql.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

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

    cursor.execute(
    "SELECT * FROM places WHERE state_id=%s",
    (state_id,)
    )

    places = cursor.fetchall()

    return render_template("places.html", places=places)


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

        place = request.form['place']
        image = request.form['image']

        cursor2 = db.cursor()

        cursor2.execute(
        "INSERT INTO place_images(place_id,image) VALUES(%s,%s)",
        (place,image)
        )

        db.commit()

        return redirect('/admin/dashboard')

    return render_template("admin/add_gallery.html", places=places)


if __name__ == "__main__":
    app.run(debug=True)