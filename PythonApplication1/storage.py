import xml.etree.ElementTree as ET
import random

class Storage:
    albumsXML = ET.parse('data/albums.xml')
    albumsRoot = albumsXML.getroot()
    usersXML = ET.parse('data/users.xml')
    usersRoot = usersXML.getroot()
    viewsXML = ET.parse('data/views.xml')
    viewsRoot = viewsXML.getroot()

    def save(self):
        #self.albumsXML.write("data/albums.xml")
        self.usersXML.write("data/users.xml")
        self.viewsXML.write("data/views.xml")

    def getUser(self, id): 
        strid = str(id)
        for user in self.usersRoot:
            if(user.get("id") == strid):
                return user
        newUser = ET.Element("user", {"id": strid})
        self.usersRoot.append(newUser)
        return newUser

    def getImage(self, user): 
        albumsCount = len(self.albumsRoot.getchildren())
        randomAlbum = self.albumsRoot[random.randint(1, albumsCount)]
        imagesCount = len(randomAlbum.getchildren())
        randomImage = randomAlbum[random.randint(1, imagesCount)]
        return randomImage

    def addView(self, user, image, score):
        newView = ET.Element('view', {"user-id": user.get("id"), "image-id": image.get("id"), "score": str(score)})
        self.viewsRoot.append(newView)

    #def addView(self, user, image_id : int, score):
    #    newView = ET.Element('view', {"user-id": user.get("id"), "image-id": str(image_id), "score": str(score)})
    #    self.viewsRoot.append(newView)

#db = Storage()
#u = db.getImage(1955062)
#print(u.text)
#db.save()

