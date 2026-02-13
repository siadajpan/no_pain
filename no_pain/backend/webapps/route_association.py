from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from starlette import status

from no_pain.backend.apis.v1.route_login import get_current_user
from no_pain.backend.db.session import get_db
from no_pain.backend.db.models.user import User
from no_pain.backend.db.models.doctor import Doctor
from no_pain.backend.db.models.practice import Practice
from no_pain.backend.db.models.user_role import UserRole

router = APIRouter(include_in_schema=False)


@router.get("/api/doctors/search")
def search_doctors(q: str = "", db: Session = Depends(get_db)):
    """Search all doctors by name. Returns JSON list."""
    doctors = (
        db.query(Doctor)
        .options(joinedload(Doctor.user))
        .join(User)
        .all()
    )
    results = []
    q_lower = q.lower()
    for doc in doctors:
        full_name = f"{doc.user.first_name} {doc.user.last_name}"
        if q_lower in full_name.lower():
            results.append({
                "id": doc.id,
                "first_name": doc.user.first_name,
                "last_name": doc.user.last_name,
                "specialization": doc.specialization or "",
                "name": full_name,
            })
    return JSONResponse(content=results)


@router.get("/api/practices/search")
def search_practices(q: str = "", db: Session = Depends(get_db)):
    """Search all practices by name. Returns JSON list."""
    practices = db.query(Practice).all()
    results = []
    q_lower = q.lower()
    for p in practices:
        name = p.name or ""
        if q_lower in name.lower():
            results.append({
                "id": p.id,
                "name": name,
                "city": p.city or "",
            })
    return JSONResponse(content=results)


@router.post("/api/practice/add-doctor")
def practice_add_doctor(
    request: Request,
    doctor_id: int = None,
    db: Session = Depends(get_db),
):
    """Practice adds a doctor to their practice."""
    user = get_current_user(request, db)
    if not user or user.role != UserRole.PRACTICE:
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    practice = user.practice
    if not practice:
        return JSONResponse(content={"error": "Practice profile not found"}, status_code=400)

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return JSONResponse(content={"error": "Doctor not found"}, status_code=404)

    if doctor in practice.doctors:
        return JSONResponse(content={"error": "Doctor already associated"}, status_code=400)

    practice.doctors.append(doctor)
    db.commit()

    return JSONResponse(content={
        "success": True,
        "doctor": {
            "id": doctor.id,
            "first_name": doctor.user.first_name,
            "last_name": doctor.user.last_name,
            "specialization": doctor.specialization or "",
        }
    })


@router.post("/api/doctor/join-practice")
def doctor_join_practice(
    request: Request,
    practice_id: int = None,
    db: Session = Depends(get_db),
):
    """Doctor joins a practice."""
    user = get_current_user(request, db)
    if not user or user.role != UserRole.DOCTOR:
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    doctor = user.doctor
    if not doctor:
        return JSONResponse(content={"error": "Doctor profile not found"}, status_code=400)

    practice = db.query(Practice).filter(Practice.id == practice_id).first()
    if not practice:
        return JSONResponse(content={"error": "Practice not found"}, status_code=404)

    if practice in doctor.practices:
        return JSONResponse(content={"error": "Already associated with this practice"}, status_code=400)

    doctor.practices.append(practice)
    db.commit()

    return JSONResponse(content={
        "success": True,
        "practice": {
            "id": practice.id,
            "name": practice.name or "",
            "city": practice.city or "",
        }
    })
