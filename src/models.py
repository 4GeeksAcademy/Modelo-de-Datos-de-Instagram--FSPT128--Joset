from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column


db = SQLAlchemy()
   

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    image: Mapped[str] = mapped_column(String(200), nullable=True) #puede o no tener imagen por eso true. 
    caption: Mapped[str] = mapped_column(String(200), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image": self.image,
            "caption": self.caption
        }
    
    
followers_table = Table(
     "followers",
    db.Model.metadata,
    Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("user.id"), primary_key=True)
)
