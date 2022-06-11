from fastapi import Depends,status,HTTPException,Response,APIRouter
from typing import Optional
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func


router=APIRouter(
    prefix="/posts",
    tags= ['Posts']
)


#GET all Posts
#@router.get("/",response_model=List[schemas.PostResponse])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user), 
limit: int=10, skip:int=0, search: Optional[str]=""):

    #cursor.execute("""SELECT * FROM posts """)
    #posts=cursor.fetchall()
    #print(current_user.email) #logged in user email

    #if you want to fetch only posts of a logged in user only or the owner of the posts, he cant ciew post from others
    #posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() 
    
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #fetch all posts from post model
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


#Get Single Post
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db),current_user :int=Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    #post=cursor.fetchone()
    #post= db.query(models.Post).filter(models.Post.id==id).first() #fetch one post with passed id
    
    post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    #if post is not found
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with Id {id} was not found!")

    # if you want to put condition that only owner of the post can view the post of given id
    #if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorised!")

    return post


#Create a Post
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))

    #created_post=cursor.fetchone()
    #conn.commit()

    created_post = models.Post(owner_id=current_user.id,**post.dict()) #create a post using sqlalchemy
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post



#Delete a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts where id = %s RETURNING *""",(str(id),))

    #deleted_post=cursor.fetchone()
    #conn.commit()
    post_query =db.query(models.Post).filter(models.Post.id==id)   #just a query to find a post with given id 
    post=post_query.first() #this actually fetches the post with given id
    
    #if post is not found
    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with Id {id} does not exist!")
    
    # if logged in users id does not match posts owner id
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not authorized for the requested action!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



# Update a post
@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE ID = %s RETURNING * """,(post.title, post.content, post.published, str(id),))

    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id) #just a query to find a post with given id 
    post=post_query.first() #  this actually fetched the post with given id

    # if post was not found
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with Id {id} does not exist!")
        
    # if logged in users id does not match posts owner id
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not authorized for the requested action!")

    post_query.update(updated_post.dict(),synchronize_session=False) #updating the post
    db.commit()

    return post_query.first()
