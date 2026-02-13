from sqlalchemy.orm import Session
from no_pain.backend.db.models.practice import Practice

def list_practices(db: Session):
    return db.query(Practice).all()

def get_practice_by_slug(slug: str, db: Session):
    # Slug format: Practice_Name (spaces replaced by underscores)
    
    practices = list_practices(db)
    for practice in practices:
        if not practice.name:
            continue
        practice_slug = practice.name.replace(" ", "_")
        if practice_slug.lower() == slug.lower():
            return practice
            
    return None
