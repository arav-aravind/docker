from fastapi import FastAPI, HTTPException
import mysql.connector
from datetime import date
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
    
@app.get("/users")
async def get_users():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
    cnx.close()
    return users

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = {"id": row[0], "name": row[1], "email": row[2]}
    cnx.close()
    return user

@app.post("/users")
async def create_user(name: str, email: str):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(query, (name, email))
    cnx.commit()
    user_id = cursor.lastrowid
    cnx.close()
    return {"id": user_id, "name": name, "email": email}

@app.put("/users/{user_id}")
async def update_user(user_id: int, name: str, email: str):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
    cursor.execute(query, (name, email, user_id))
    cnx.commit()
    cnx.close()
    return {"id": user_id, "name": name, "email": email}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    cnx.commit()
    cnx.close()
    return {"message": "User deleted"}