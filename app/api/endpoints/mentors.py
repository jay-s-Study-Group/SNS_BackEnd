from fastapi import APIRouter, Response, Form, File, UploadFile
from app.schemas import (
    ApplicationMentoringSchema,
    ApplicationMentoringResponseSchema
)
from app.controllers.mentorings import MentoringController
from starlette import status

router = APIRouter()

@router.post(
    "/register-mentoring", response_model=ApplicationMentoringResponseSchema, status_code=status.HTTP_201_CREATED
)
def register(user_id: int, application_mentoring_info: ApplicationMentoringSchema):
    """
    `ENG subscribe: Request mentoring by selecting the price, capacity, field, etc.` \n
    `KOR subscribe: 가격, 수용인원, 필드등을 골라 멘토링을 신청합니다.`
    ### body (json)
    - **email** : str = user email (should be unique)
    - **password** : str = user password (must be at least 8 letters long)
    """
    return MentoringController().register_mentoring_class(user_id, application_mentoring_info)

@router.post(
    "/classroom", response_model=ApplicationMentoringResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_classroom(user_id: int, mentoring_id:int = Form(...), classroom_type_name: str = Form(...)
                                            , content: str = Form(...), file: UploadFile = File(...)):
    return MentoringController().create_classromm(user_id, mentoring_id, classroom_type_name, content,
                                                  file)

@router.get(
    "/mentoring", response_model=ApplicationMentoringResponseSchema, status_code=status.HTTP_201_CREATED
)
def search_mentoring(user_id: int, mentoring_field, count=10, page=1):
    return MentoringController().get_mentoring_info(user_id, mentoring_field, count, page)