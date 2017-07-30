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
def hello_world():
    albom = Albom(1)
    albom.add(Look(1,"http://i.imgur.com/EmFMZvu.jpg"))
    albom.add(Look(2,"http://i.imgur.com/hTFDTz4.jpg"))
    look = Look(3, "http://i.imgur.com/VG48nre.jpg")
    albom.add(look)

    albom = Albom(2)
    albom.add(Look(1,"http://i.imgur.com/UPEIjYW.jpg"))
    albom.add(Look(2,"http://i.imgur.com/hY1atQv.jpg"))
    albom.add(Look(3,"http://i.imgur.com/fmpSvw6.jpg"))

    albom = Albom(3)
    albom.add(Look(1,"http://i.imgur.com/pUrKJ9v.jpg"))
    albom.add(Look(2,"http://i.imgur.com/sHmWhY2.jpg"))
    albom.add(Look(3,"http://i.imgur.com/vL1Iv83.jpg"))

    return render_template("test.html", look = look)

@app.route('/like/<id>')
def like_look():
    pass



@app.route('/dislike/<id>')
def dislike_look():
    pass



if __name__ == '__main__':
    app.run()
