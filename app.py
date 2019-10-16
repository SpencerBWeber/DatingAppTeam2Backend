from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vynrwhtdwrblyq:ba20c760fef6273a0465282cf8ed6040a16f49e127f1965a381409983d19f354@ec2-50-19-95-77.compute-1.amazonaws.com:5432/d3f0b8ca4ih6cg'

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False)
    last_name = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(999))
    isAdmin = db.Column(db.Boolean(False))

    def __init__(self, first_name, last_name, username, password, profile_picture, isAdmin):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.profile_picture = profile_picture
        self.isAdmin = isAdmin


class UserSchema(ma.Schema):
    class Meta:
        fields = ('first_name', "last_name", "username",
                  "password", "profile_picture", "isAdmin")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user', methods=['POST'])
def add_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    password = request.json['password']
    profile_picture = request.json['profile_picture']
    isAdmin = request.json['isAdmin']

    new_user = User(first_name, last_name, username,
                    password, profile_picture, isAdmin)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)


@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route('/user/<id>', methods=['PUT'])
def user_update(id):
    user = User.query.get(id)
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    password = request.json['password']
    profile_picture = request.json['profile_picture']
    isAdmin = request.json['isAdmin']

    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.password = password
    user.profile_picture = profile_picture
    user.isAdmin = isAdmin

    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/user/<id>', methods=['DELETE'])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return "User was successfully deleted"


class Headline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(100), unique=False)
    subheading = db.Column(db.String(100), unique=False)
    author = db.Column(db.String(100), unique=False)
    article = db.Column(db.String(5000), unique=False)
    image_url = db.Column(db.String(999), unique=False)

    def __init__(self, headline, subheading, author, article, image_url):
        self.headline = headline
        self.subheading = subheading
        self.author = author
        self.article = article
        self.image_url = image_url


class HeadlineSchema(ma.Schema):
    class Meta:
        fields = ('headline', 'subheading', 'author', 'article', 'image_url')


headline_schema = HeadlineSchema()
headlines_schema = HeadlineSchema(many=True)


@app.route('/headline', methods=['POST'])
def add_headline():
    headline = request.json['headline']
    subheading = request.json['subheading']
    author = request.json['author']
    article = request.json['article']
    image_url = request.json['image_url']

    new_headline = Headline(headline, subheading, author, article, image_url)

    db.session.add(new_headline)
    db.session.commit()

    headline = Headline.query.get(new_headline.id)

    return headline_schema.jsonify(headline)


@app.route('/headlines', methods=['GET'])
def get_headlines():
    all_headlines = Headline.query.all()
    result = headlines_schema.dump(all_headlines)

    return jsonify(result)


@app.route('/headline/<id>', methods=['GET'])
def get_headline(id):
    headline = Headline.query.get(id)
    return headline_schema.jsonify(headline)


@app.route('/headline/<id>', methods=['PUT'])
def update_headline(id):
    report = Headline.query.get(id)
    headline = request.json['headline']
    subheading = request.json['subheading']
    author = request.json['author']
    article = request.json['article']
    image_url = request.json['image_url']

    report.headline = headline
    report.subheading = subheading
    report.author = author
    report.article = article
    report.image_url = image_url

    db.session.commit()
    return headline_schema.jsonify(report)


@app.route('/headline/<id>', methods=['DELETE'])
def headline_delete(id):
    headline = Headline.query.get(id)
    db.session.delete(headline)
    db.session.commit()

    return "Headline successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)
