from flask import Flask
from flask import render_template

app = Flask(__name__)

class Look:
    def __init__(self, id, img_url):
        self.id = id
        self.img_url = img_url

class Albom:
    def __init__(self, id):
        self.id = id
        self.looks = []
    def add(self, look:Look):
        self.looks.append(look)

class DeBe:
    def __init__(self):
        self.alboms = []
    def add(self, albom:Albom):
        self.alboms.append(albom)

    def get_next_look(self):
        return self.alboms[0].looks[0];

@app.route('/')
@app.route('/index')
@app.route('/user/<username>')

@app.route('/like/<id>')
def like_look():
    pass



@app.route('/dislike/<id>')
def dislike_look():
    pass



if __name__ == '__main__':
    app.run()
