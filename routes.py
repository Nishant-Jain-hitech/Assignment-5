from schemas import EagerAuthorResponseModel, EagerBlogResponseModel
from helper import filter_by_category
from helper import blog_not_found, author_not_found, paginate
from datetime import datetime
from fastapi import Depends
from fastapi import APIRouter
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models import Author, AuthorProfile, Blog, Category, BlogCategory


router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health_status():
    return {"status": "ok"}


@router.post("/seed")
def add_data(db: Session = Depends(get_db)):
    author = Author(
        name="Nishant",
        email="email@email.com",
        author_profile=AuthorProfile(bio="FastAPI aa gyi bhai!"),
    )

    author.blogs.append(
        Blog(title="Blog1", content="Blog1 ka content", published_at=datetime.now())
    )
    author.blogs.append(
        Blog(title="Blog2", content="Blog2 ka content", published_at=datetime.now())
    )
    author.blogs.append(
        Blog(title="Blog3", content="Blog3 ka content", published_at=datetime.now())
    )

    category1 = Category(name="category1")
    category2 = Category(name="category2")

    author.blogs[0].blog_categories.append(BlogCategory(category=category1))
    author.blogs[1].blog_categories.append(BlogCategory(category=category2))
    author.blogs[2].blog_categories.append(BlogCategory(category=category1))

    db.add(author)
    db.commit()
    return {"message": "Data added successfully"}


@router.get("/eager/author/{author_id}", response_model=EagerAuthorResponseModel)
def get_author(author_id: int, db: Session = Depends(get_db)):

    author_not_found(db, author_id)

    author = (
        db.query(Author)
        .options(
            joinedload(Author.author_profile),
            joinedload(Author.blogs)
            .joinedload(Blog.blog_categories)
            .joinedload(BlogCategory.category),
        )
        .filter(Author.id == author_id)
        .first()
    )

    return {
        "name":author.name,
        "profile":author.author_profile.bio if author.author_profile.bio else None,
        "blogs":[{
            "title":blog.title,
            "categories":[category.category.name for category in blog.blog_categories]
        }for blog in author.blogs]
    }


@router.get("/eager/blog/{blog_id}",response_model=EagerBlogResponseModel)
def get_blog(blog_id: int, db: Session = Depends(get_db)):

    blog_not_found(db, blog_id)

    blog = (
        db.query(Blog)
        .options(
            joinedload(Blog.author),
            joinedload(Blog.blog_categories).joinedload(BlogCategory.category),
        )
        .filter(Blog.id == blog_id)
        .first()
    )

    return {
        "title":blog.title,
        "author":blog.author.name,
        "categories":[category.category.name for category in blog.blog_categories]
    }


@router.get("/blogs")
def get_blogs(page: int|None = None, limit: int|None = None, category:str|None=None, db: Session = Depends(get_db)):
    if page and limit:
        return paginate(db,page,limit)

    if category:
        return filter_by_category(db,category)

    