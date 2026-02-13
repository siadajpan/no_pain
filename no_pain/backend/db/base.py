from no_pain.backend.db.base_class import Base  # noqa

# Import all models here
from no_pain.backend.db.models.user import User  # noqa
from no_pain.backend.db.models.user_verification import UserVerification  # noqa
from no_pain.backend.db.models.doctor import Doctor  # noqa
from no_pain.backend.db.models.patient import Patient  # noqa
from no_pain.backend.db.models.practice import Practice  # noqa
from no_pain.backend.db.models.associations import practice_doctor, practice_patient  # noqa

