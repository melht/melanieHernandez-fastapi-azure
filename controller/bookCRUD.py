from typing import List

from fastapi import HTTPException, APIRouter
from db.db import collection
from model.book import Book

router = APIRouter()

# Add book
@router.post("/", response_description="Add new book", response_model= Book)
async def create_book(book: Book):
    existing_book = await collection.find_one({"isbn": book.isbn})
    if existing_book != None:
        raise HTTPException(status_code=400, detail="ISBN already exists")
    result = await collection.insert_one(book.dict())
    book._id = str(result.inserted_id)
    return book


@router.get("/", response_description="Show all books", response_model= List[Book])
async def read_books():
    books = await collection.find().to_list(100)
    for book in books:
        book["_id"] = str(book["_id"])
    return books

# Find book
@router.get("/{isbn}", response_model=Book)
async def find_book_isbn(isbn: str):
    book = await collection.find_one({"isbn": isbn})

    if book:
        return book
    raise HTTPException(status_code=404, detail="The book was not found")

# Update book
@router.put("/{isbn}", response_model=Book)
async def update_book(isbn: str, book: Book):
    updated_book = await collection.find_one_and_update(
        {"isbn": isbn}, {"$set": book.dict()}
    )
    if updated_book:
        return book
    raise HTTPException(status_code=404, detail="The book was not found")

# Delete book
@router.delete("/{isbn}", response_model=Book)
async def delete_book(isbn: str):
    deleted_book = await collection.find_one_and_delete({"isbn": isbn})
    if deleted_book:
        return deleted_book
    raise HTTPException(status_code=404, detail="The book was not found")
