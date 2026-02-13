from sqlalchemy.orm import Session, joinedload
from no_pain.backend.db.models.doctor import Doctor
from no_pain.backend.db.models.user import User

def list_doctors(db: Session):
    doctors = db.query(Doctor).options(joinedload(Doctor.user)).join(User).all()
    print(f"DEBUG: Found {len(doctors)} doctors.")
    for d in doctors:
        print(f"DEBUG: Doc: {d.user.first_name} {d.user.last_name}")
    return doctors

def get_doctor_by_slug(slug: str, db: Session):
    # Slug format: Firstname_Lastname
    # We need to reconstruct this search. 
    # Since specific slug logic (replacing spaces with underscores) is in the view/template,
    # we might need to iterate or be smart about the query.
    # For MVP, assume strict "Firstname_Lastname" matching.
    
    if "_" not in slug:
        return None
        
    parts = slug.split("_")
    # What if name has multiple parts? "Jean_Claude_Van_Damme"
    # Basic assumption: Last part is last name, everything else is first name? 
    # Or just iterate all docs and match python-side (slow but safe for MVP)?
    # Or strict: First Name (can be multiple words) and Last Name (can be multiple words).
    # Let's try to match by constructing the slug in python for all docs.
    
    doctors = list_doctors(db)
    for doc in doctors:
        doc_slug = f"{doc.user.first_name}_{doc.user.last_name}".replace(" ", "_")
        if doc_slug.lower() == slug.lower():
            return doc
            
    return None
