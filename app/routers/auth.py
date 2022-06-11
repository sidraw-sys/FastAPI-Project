from fastapi import Depends,status,HTTPException,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models,schemas,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(login_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email == login_credentials.username).first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials!")
    
    if utils.verify(login_credentials.password, user.password) == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials!")

    #create token
    access_token = oauth2.create_access_token({'user_id':user.id})
    #return token

    return {"access_token": access_token, "token_type":"bearer"}

