from app.models import User, SocialAuth
from app.schemas import CreateSocialUserSchema
from app.databases.session import db


@db.db_connect
def get_user_by_sns_service_id(sns_service_id: str):
    social_auth_instance = SocialAuth.filter(
        SocialAuth.sns_service_id == sns_service_id
    ).first()
    if social_auth_instance is None:
        raise Exception()
    user_instance = User.filter(User.id == social_auth_instance.user).first()
    return user_instance


@db.db_connect
def create_social_auth(user: User, sns_service_id: str, platform: str):
    social_auth_instance = SocialAuth(
        platform=platform, sns_service_id=sns_service_id, user=user
    )
    social_auth_instance.save()
    return social_auth_instance


@db.db_connect
def create_social_user(
    user: CreateSocialUserSchema, sns_service_id: str, platform: str
):
    user_instance = User(
        email=user.email, sns_service_id=sns_service_id, platform=platform
    )
    return user_instance
