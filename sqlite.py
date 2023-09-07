# import sqlite3 as sq


# async def db_start():
#     global db, cur

#     db = sq.connect("new.db")
#     cur = db.cursor()
    
#     cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY)")

#     db.commit()