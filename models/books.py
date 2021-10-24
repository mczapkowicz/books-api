from mongoengine import Document, StringField


class Books(Document):
    _id = StringField()
    name = StringField()
    author = StringField()

    def to_json(self):
        return {
            "_id": str(self._id),
            "name": self.name,
            "author": self.author,
        }