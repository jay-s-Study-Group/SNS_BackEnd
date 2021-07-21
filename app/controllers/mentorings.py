from playhouse.shortcuts import model_to_dict

from app.core.utils import exceptions as ex
from app.models.users import (
    User,
    MentoringField,
)
from app.models.mentorings import (
    MentorApplication, ClassRoom, ClassRoomType
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

    def create_classromm(self, user_id, mentoring_id, classroom_type_name, content,
                                                  file):
        exist_user = self.get_user_by_id(user_id)

        if exist_user is None:
            raise ex.NotFoundUserEx(user_id)

        mentoring = MentorApplication.get_or_none(MentorApplication.id == mentoring_id)
        if mentoring is None:
            raise ex.NotFoundMentoringEx(user_id, mentoring_id)

        class_type_info = ClassRoomType.get_or_none(ClassRoomType.type_name == classroom_type_name)
        if class_type_info is None:
            raise ex.NotFoundClassTypeEx(user_id, mentoring_id)

        #todo s3 에 파일 올려서 s3경로 저장하도록 수정
        data = dict(
            mentoring_id=mentoring_id,
            classroom_type=class_type_info.id,
            content=content,
            content_file=None
        )

        return model_to_dict(ClassRoom.create(data))

    def get_mentoring_info(self, user_id, mentoring_field, count, page):
        exist_user = self.get_user_by_id(user_id)

        if exist_user is None:
            raise ex.NotFoundUserEx(user_id)

        query = MentorApplication.select()
        if mentoring_field:
            query = query.where(MentorApplication.mentoringfield == mentoring_field)

        result = [model_to_dict(x) for x in query.paginate(page, count).execute()]

        return result