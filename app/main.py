from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from random import randrange
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from . import models
from .database import engine
from .routers import post,user,auth,vote

#tells sqlalchemy to creat the tables present inside models.py into our database
#models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print({'msg':'Welcome to Fastapi...'})

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# connecting to Postgres database
""" while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='admin123',cursor_factory=RealDictCursor)
        cursor= conn.cursor()
        print("Database connection successful")
        break

    except Exception as error:
        print("Connection to Database failed!")
        print("Error:",error)
        time.sleep(2) """
    

""" my_posts=[{"title":"Post 1","content":"Content of Post 1","id":1 },
          {"title":"Post 2","content":"Content of Post 2","id":2 },
          {"title":"Post 3","content":"Content of Post 3","id":3 }  
         ] """



""" def find_post(id):
    for post in my_posts:
        if post['id']==id:
            return post

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i """




    
    
    
    
    

    






