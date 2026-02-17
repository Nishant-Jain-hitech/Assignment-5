from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)

    author_profile = relationship(
        "AuthorProfile",
        back_populates="author",
        uselist=False,
        cascade="all, delete-orphan",
    )

    blogs = relationship("Blog", back_populates="author")


class AuthorProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String)

    author_id = Column(
        Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )

    author = relationship("Author", back_populates="author_profile")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)

    published_at = Column(DateTime, nullable=True) 

    author_id = Column(
        Integer, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True
    )

    author = relationship("Author", back_populates="blogs")

    blog_categories = relationship(
        "BlogCategory", back_populates="blog", cascade="all, delete-orphan"
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    blog_categories = relationship(
        "BlogCategory", back_populates="category", cascade="all, delete-orphan"
    )


class BlogCategory(Base):
    __tablename__ = "blog_categories"

    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(
        Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )

    blog = relationship("Blog", back_populates="blog_categories")
    category = relationship("Category", back_populates="blog_categories")
