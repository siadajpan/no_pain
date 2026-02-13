import enum

class UserRole(str, enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    PRACTICE = "practice"
