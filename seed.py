import sqlite3
import random
import string

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM drawings")
db.execute("DELETE FROM likes")

user_count = 1000
drawing_count = 100000

print("Inserting users...")
for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
               [f"user{i}", "fakehash"])

print("Inserting drawings...")
dummy_payload = "0" * 100 

for i in range(1, drawing_count + 1):
    username = f"user{random.randint(1, user_count)}"
    db.execute("INSERT INTO drawings (username, title, payload) VALUES (?, ?, ?)", 
               [username, f"Drawing {i}", dummy_payload])

print("Committing...")
db.commit()
db.close()
print("Done")