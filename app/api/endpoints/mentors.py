from fastapi import APIRouter, Response
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

