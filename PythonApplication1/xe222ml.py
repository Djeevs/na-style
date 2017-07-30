import xml.etree.ElementTree as ET

class DEBE:
    tree = ET.parse('data/debe.xml')
    root = tree.getroot()

    def save(self):
        self.tree.write("data/debe.xml")

    def get_user(self, id): 
        users = self.root.find("users")
        for user in users:
            if(user.get("id") == id):
                return user
        newUser = ET.Element("user", {"id": str(id)})
        users.append(newUser)
        return newUser

    def add_view(self, user, image, score):
        views = self.root.find("views")
        newView = ET.Element('view', {"user-id": user.get("id"), "image-id": image.get("id"), "score": str(score)})
        views.append(newView)

    def add_view(self, user, image_id : int, score):
        views = self.root.find("views")
        newView = ET.Element('view', {"user-id": user.get("id"), "image-id": str(image_id), "score": str(score)})
        views.append(newView)
