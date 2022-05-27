from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.core.conf import AppConf
from app.core.exceptions import DatabaseError

Base = declarative_base()


class Database:
    def __init__(self, conf: AppConf) -> None:
        self._engine = create_engine(conf.db_url)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(
        self, session: Session = None
    ) -> Callable[..., AbstractContextManager[Session]]:
        if session is not None:
            # user has to handle session themselve
            yield session

        session: Session = self._session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise DatabaseError(error_details=e)
        finally:
            session.close()
