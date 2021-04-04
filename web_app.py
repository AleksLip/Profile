from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/profiles')
def profiles():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("profiles.html", articles=articles)


@app.route('/profiles/<int:id>')
def profile_details(id):
    article = Article.query.get(id)
    return render_template("profile_details.html", article=article)


@app.route('/profiles/<int:id>/delete')
def profile_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/profiles')
    except:
        return "There was an issue"


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        profile = request.form['profile']
        status = request.form['status']

        article = Article(name=name, surname=surname, profile=profile, status=status)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/profiles')
        except:
            return "There was an issue"
    else:
        return render_template("create.html")

@app.route('/profiles/<int:id>/update', methods=['POST', 'GET'])
def profile_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.name = request.form['name']
        article.surname = request.form['surname']
        article.profile = request.form['profile']
        article.status = request.form['status']

        try:
            db.session.commit()
            return redirect('/profiles')
        except:
            return "There was an issue when updating"
    else:
        return render_template("profile_update.html", article=article)


if __name__ == "__main__":
    app.run(debug=True)

#import tsp
#matrix=[[1,2,3,4],
#        [5,6,7,8],
#        [9,10,11,12],
#        [13,14,15,16]]
#r=range(len(matrix))

#shortestpath={(i,j):matrix[i][j] for i in r for j in r}
#print(tsp.tsp(r,shortestpath))