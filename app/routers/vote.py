from fastapi import Depends,status,HTTPException,Response,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(prefix='/vote',tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(vote.post_id==models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} does not exist!")
    
    vote_query=db.query(models.Vote).filter(vote.post_id==models.Vote.post_id, current_user.id==models.Vote.user_id)
    found_vote=vote_query.first()
    

    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Post with id {vote.post_id} has already been liked by user id {current_user.id}")
            
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"Post liked successfully!"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Can't delete like, Post with id {vote.post_id} has not been liked by user id {current_user.id} yet.")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Post Unliked successfully!"}
    
