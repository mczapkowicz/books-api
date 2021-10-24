from mongoengine import Document, StringField


class Users(Document):
    _id = StringField()
    name = StringField()
    email = StringField()
    password = StringField()

    def to_json(self):
        return {
            "_id": str(self._id),
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }