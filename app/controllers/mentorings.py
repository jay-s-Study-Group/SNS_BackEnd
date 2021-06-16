from app.core.utils import exceptions as ex
from app.models.users import (
    User,
    MentoringField,
)
from app.models.mentorings import (
    MentorApplication
)


class MentoringController:
    def __init__(self):
        pass

    def get_user_by_id(self, user_id: int) -> User:
        user_instance = User.filter(User.id == user_id).first()
        return user_instance

    def register_mentoring_class(self, user_id, application_mentoring_info):
        application_mentoring_info = application_mentoring_info.__dict__

        exist_user = self.get_user_by_id(user_id)

        if not exist_user:
            raise ex.NotFoundUserEx(user_id)

        if mentoring_fields := application_mentoring_info["mentoring_fields"]:
            for field in mentoring_fields:
                if mentoring_filed_value := MentoringField.filter(MentoringField.field == field).first():
                    mentoring_field = MentoringField.create(
                        field=MentoringField.field).field if mentoring_filed_value is None else mentoring_filed_value.field

        application_mentoring_info['mentoringfield'] = str(mentoring_field)
        application_mentoring_info['user_id'] = user_id
        MentorApplication.create(application_mentoring_info)

        return application_mentoring_info