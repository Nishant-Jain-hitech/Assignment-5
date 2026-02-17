from models import Author, Blog, BlogCategory, Category
from fastapi import HTTPException


def author_not_found(db, author_id):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author nhi h bhai")
    return author


def blog_not_found(db, blog_id):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog nhi h bhai")
    return blog


def paginate(db, page, limit):
    if not page or not limit:
        return db.query(Blog).all()
    blogs = db.query(Blog).all()
    return blogs[(page - 1) * limit : page * limit]


def filter_by_category(db, category):
    category_blogs = (
        db.query(Blog)
        .join(BlogCategory)
        .join(Category)
        .filter(Category.name == category)
        .all()
    )
    return category_blogs
