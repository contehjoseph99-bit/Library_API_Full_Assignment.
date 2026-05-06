from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

books = {
    1: {"title": "Python Basics", "available": True}
}

borrowed_books = {}

@app.get("/books")
async def get_books():
    return books

@app.post("/borrow")
async def borrow_book(user_id: int, book_id: int):
    if books[book_id]["available"]:
        books[book_id]["available"] = False
        due_date = datetime.now() + timedelta(days=7)
        borrowed_books[book_id] = {"user_id": user_id, "due_date": due_date}
        return {"message": "Book borrowed", "due_date": str(due_date)}
    return {"message": "Book not available"}

@app.post("/return")
async def return_book(user_id: int, book_id: int):
    if book_id in borrowed_books:
        books[book_id]["available"] = True
        del borrowed_books[book_id]
        return {"message": "Book returned"}
    return {"message": "Book not borrowed"}

@app.get("/overdue")
async def overdue():
    today = datetime.now()
    result = []
    for book_id, info in borrowed_books.items():
        if info["due_date"] < today:
            result.append({"user_id": info["user_id"], "book_id": book_id})
    return {"overdue": result}
