from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

followers_table = Table(
    "followers",
    db.Model.metadata,
    Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("user.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    
    following: Mapped[List["User"]] = relationship(
        secondary=followers_table,
        primaryjoin=(followers_table.c.follower_id == id),
        secondaryjoin=(followers_table.c.following_id == id),
        backref=db.backref('followers'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__ = "post"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    image: Mapped[str] = mapped_column(String(200), nullable=True) 
    caption: Mapped[str] = mapped_column(String(200), nullable=False)

    user: Mapped["User"] = relationship(back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image": self.image,
            "caption": self.caption
        }

class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(200), nullable=False)

    user: Mapped["User"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "text": self.text
        }







# class User(db.Model):
#    class User(db.Model):
#     __tablename__ = "user"
#     __table_args__ = {'extend_existing': True}
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(String(250), nullable=False)
#     name: Mapped[str] = mapped_column(String(120), nullable=True)

#     posts: Mapped[List["Post"]] = relationship(back_populates="user")
#     comments: Mapped[List["Comment"]] = relationship(back_populates="user")
#     followed: Mapped[List["User"]] = relationship(
#         secondary=followers_table,
#         primaryjoin=(followers_table.c.follower_id == id),
#         secondaryjoin=(followers_table.c.followed_id == id),
#         back_populates='followers_by'
#     )


#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             "name": self.name,
#             "followers": self.favorites
#             # do not serialize the password, its a security breach
#         }

# class Post(db.Model):
#     __tablename__ = "post"
#     __table_args__ = {'extend_existing': True}
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
#     image: Mapped[str] = mapped_column(String(200), nullable=True)  #puede o no tener imagen por eso true. 
#     caption: Mapped[str] = mapped_column(String(200), nullable=False)

#     user: Mapped["User"] = relationship(back_populates="posts")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "image": self.image,
#             "caption": self.caption
#         }

# class Comment(db.Model):
#     __tablename__ = "comment"
#     __table_args__ = {'extend_existing': True}
#     id: Mapped[int] = mapped_column(primary_key=True)
#     post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
#     text: Mapped[str] = mapped_column(String(200), nullable=False)

#     user: Mapped["User"] = relationship(back_populates="comments")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "post_id": self.post_id,
#             "user_id": self.user_id,
#             "text": self.text
#         }
