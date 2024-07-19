import os
from flask import Flask, render_template, request, redirect, url_for, Response
import json
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv() # makes .env credentials available
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
              user=os.getenv("MYSQL_USER"),
              password=os.getenv("MYSQL_PASSWORD"),
              host=os.getenv("MYSQL_HOST"),
              port=3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])


# Example data for display
work_experiences = []
educations = []
hobbies = []

@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
    )

@app.route("/work", methods=["GET", "POST"])
def work():
    # This handles the POST requests to add a new work experience and education.
    # It extracts data from the form and appends it to the 'work_experiences' and 'educations' list.
    # Then, it redirects back to the index page after adding.
    if request.method == "POST":
        if "title" in request.form:
            new_experience = {
                "title": request.form["title"],
                "company": request.form["company"],
                "location": request.form["location"],
                "duration": request.form["duration"],
                "description": request.form["description"],
            }
            work_experiences.append(new_experience)
        elif "degree" in request.form:
            new_education = {
                "degree": request.form["degree"],
                "university": request.form["university"],
                "location": request.form["location"],
                "duration": request.form["duration"],
                "description": request.form["description"],
            }
            educations.append(new_education)
        return redirect(url_for("work"))

    return render_template(
        "work.html",
        title="Work and Education",
        work_experiences=work_experiences,
        educations=educations,
        url=os.getenv("URL"),
    )

@app.route('/hobbies', methods=['GET', 'POST'])
def hobbies_page():
    if request.method == 'POST':
        new_hobby = {
            "name": request.form["name"],
            "description": request.form["description"],
        }
        hobbies.append(new_hobby)
        return redirect(url_for('hobbies_page'))
    return render_template('hobbies.html', title="Hobbies", hobbies=hobbies, url=os.getenv("URL"))



@app.route('/places')
def places():
    return render_template('places.html', title="MLH Fellow", url=os.getenv("URL"))


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return Response(
            json.dumps({"error": "Invalid name"}),
            status=400,
            mimetype='application/json'
        )
    if not content:
        return Response(
            json.dumps({"error": "Invalid content"}),
            status=400,
            mimetype='application/json'
        )
    if not email or "@" not in email:
        return Response(
            json.dumps({"error": "Invalid email"}),
            status=400,
            mimetype='application/json'
        )

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    post_dict = model_to_dict(timeline_post)
    post_dict['created_at'] = post_dict['created_at'].strftime('%Y-%m-%dT%H:%M:%S')
    return Response(
        json.dumps(post_dict),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    posts = [
        model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]
    for post in posts:
        post['created_at'] = post['created_at'].strftime('%Y-%m-%dT%H:%M:%S')  # Convert datetime to string
    return Response(
        json.dumps({'timeline_posts': posts}),
        status=200,
        mimetype='application/json'
    )
@app.route('/timeline')
def timeline():
    response = get_time_line_post()
    time_line_messages = json.loads(response.get_data(as_text=True))['timeline_posts']
    return render_template('timeline.html', title="Timeline", time_line_messages=time_line_messages)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                         user=os.getenv("MYSQL_USER"),
                         password=os.getenv("MYSQL_PASSWORD"),
                         host=os.getenv("MYSQL_HOST"),
                         port=3306
                         )
                         