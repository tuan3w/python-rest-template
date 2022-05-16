from app.core.database import Base
from app.modules.auth.model import User
from sqlalchemy import Column, Integer
from tests.utils import init_test_container


class InvalidModel(Base):
    __tablename__ = 'notfound'
    id = Column(Integer, primary_key=True)


def test_db_session_rollback():
    container = init_test_container()
    db = container.db()
    user_repo = container.user_repo()

    usecase = container.auth.register()
    with db.session() as session:
        try:
            u1 = usecase.register('test', 'test', user_id=1, shared_session=session)
            u1 = usecase.register('test', 'test', user_id=1, shared_session=session)
            session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

    user = user_repo.get_user_by_username('test')
    assert user == None

    user = usecase.register('test', 'test', user_id=1)
    user = user_repo.get_user_by_username('test')
    assert user != None