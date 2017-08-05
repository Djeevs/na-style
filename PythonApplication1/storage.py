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
            if user.get("id") == strid:
                return user
        newUser = ET.Element("user", {"id": strid})
        self.usersRoot.append(newUser)
        return newUser



    def getImage(self, user): 

        def getCount(iterable, sfinctor):
            count = 0;
            for i in iterable:
                if(sfinctor(i)):
                    count += 1
            return count

        
        

        views = []
        for view in self.viewsRoot:
            if view.get("user-id") == user.get("id"):
                views.append(view)
        viewsAlbums = list(map(lambda v : v.get("album-id"), views))
        viewsImages = list(map(lambda v : v.get("image-id"), views))
        

        albumsCount = getCount(self.albumsRoot, lambda i : True)
        albumsNeverViewedCount = getCount(self.albumsRoot, 
                                          lambda a : a.get("id") not in viewsAlbums)

        albumScores = []
        for album in self.albumsRoot:
            likeCount = getCount(views, lambda v : v.get("album-id") == album.get("id") and v.get("score") == "1")
            dislikeCount = getCount(views, lambda v : v.get("album-id") == album.get("id") and v.get("score") == "-1")
            imageCount = len(album.getchildren())

            score = -1
            if imageCount == likeCount + dislikeCount : score = 0
            elif likeCount + dislikeCount == 0 : score = 0.1 / (albumsNeverViewedCount + 1)
            elif likeCount + dislikeCount >= 4 and likeCount / (likeCount + dislikeCount) <= 0.2 : score = 0
            else : score = max(0.2, likeCount / (likeCount + dislikeCount))
            
            albumScores.append((album, score))
           
        totalScore = sum(map(lambda s : s[1], albumScores))
        
        albumScores = list(map(lambda kv: (kv[0], kv[1]/totalScore), albumScores))
        
        prob = random.uniform(0, 1)

        selectedAlbum = None
        for a in albumScores:
            prob -= a[1]
            if(prob < 0):
                selectedAlbum = a[0]
                break

        notViewedImages = list(filter(lambda f : f.get("id") not in viewsImages, map(lambda a : a, selectedAlbum.getchildren())))

        randomImage = notViewedImages[random.randint(0, len(notViewedImages))]

        return selectedAlbum, randomImage

    def addView(self, user, album, image, score):
        newView = ET.Element('view', {"user-id": user.get("id"), "image-id": image.get("id"), "album-id": album.get("id"), "score": str(score)})
        self.viewsRoot.append(newView)

    

    #def addView(self, user, image_id : int, score):
    #    newView = ET.Element('view', {"user-id": user.get("id"), "image-id": str(image_id), "score": str(score)})
    #    self.viewsRoot.append(newView)

#db = Storage()
#u = db.getUser(38051857)
#i = db.getImage(u)
#print(u)
#print(u.text)
#db.save()

