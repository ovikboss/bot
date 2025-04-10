from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select, or_
from .models import Base, User, Message, Language
from datetime import date
import logging


from .config import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:

    def __init__(self):
        settings = Settings()
        self.engine = create_engine(
            f"postgresql+psycopg2://{settings.USER}:{settings.PASSWORD}@db:{settings.PORT}/{settings.DBNAME}",
            isolation_level="READ COMMITTED",
        )
        Base.metadata.create_all(self.engine)

    def create_user(self, telegram_id):
        with Session(self.engine) as session:
            user = (
                    session.query(User)
                    .filter(User.telegram_id == str(telegram_id))
                    .first()
                )
            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)
                session.commit()

    def find_user(self, telegram_id):
        try:
            with Session(self.engine) as session:
                user = (
                    session.query(User)
                    .filter(User.telegram_id == str(telegram_id))
                    .first()
                )
                if user:
                    users = (
                        session.query(User)
                        .filter(
                            User.date_of_birth == user.date_of_birth,
                            User.telegram_id
                            != str(telegram_id),  # Exclude the user himself
                        )
                        .all()
                    )
                    logger.info(
                        f"Found users with the same birthdate as user {telegram_id}"
                    )
                    return users
                else:
                    logger.warning(f"User with telegram_id {telegram_id} not found.")
                    return []  # or None, depending on desired behavior
        except Exception as e:
            logger.error(f"Error finding user with telegram_id {telegram_id}: {e}")
            return []

    def get_users(self):
        """Получает список telegram_id всех пользователей."""
        try:
            with Session(self.engine) as session:
                users = session.query(
                    User.telegram_id
                ).all()  # Получаем только telegram_id
                user_ids = [
                    user[0] for user in users
                ]  # Преобразуем в список telegram_id
                logger.info(f"Found users: {user_ids}")
                return user_ids
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []

    def send_message(self, message, recipient_id, telegram_id):
        with Session(self.engine) as session:
            message = Message(text=message, recipient_id=recipient_id, user=telegram_id)
            session.add(message)
            session.commit()

    def set_name_and_date(self, telegram_id, date_of_bird, name):
        with Session(self.engine) as session:
            user = (
                session.query(User).filter(User.telegram_id == str(telegram_id)).first()
            )
            print(user)
            user.date_of_birth = date_of_bird
            user.name = name
            session.commit()

    def set_user_language(self, telegram_id: int, language_code: str):

        with Session(self.engine) as session:
            user = (
                session.query(User).filter(User.telegram_id == str(telegram_id)).first()
            )
            if user:
                user.language = Language(language_code)
                session.commit()
                print(f"Language set to {language_code} for user {telegram_id}")
            else:
                print(f"User not found with telegram_id {telegram_id}")

    def get_user_language(self, telegram_id: str):
        with Session(self.engine) as session:
            user_language = session.query(User.language).filter(User.telegram_id == str(telegram_id)).first()
            return user_language[0]


db = Database()
# result = db.find_user(1234, "23-03-1999")
# db.start_chat(1,2)
