from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func 
from typing import List, Optional

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: str = Depends(utils.get_current_user), 
             limit: int = 25, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = list ( map (lambda x : x._mapping, results) )
    print(results)
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(utils.get_current_user)):
    #post_dict["id"] = randrange(0, 1000000)
    #post_dict = post.dict()
    #my_posts.append(post_dict)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(utils.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()   

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID ({id}) was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND      
        # return {"message": f"Post with ID ({id}) was not found"}  
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(utils.get_current_user)):
    
    #index = find_index_post(id)
    #if index == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID ({id}) was not found")
    #my_posts.pop(index)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(utils.get_current_user)):
    #print(post)
#
    #index = find_index_post(id)
    #if index == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID ({id}) was not found")
    #
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID ({id}) does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
        
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()