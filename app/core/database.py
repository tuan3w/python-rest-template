from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.core.conf import AppConf
from app.core.exceptions import DatabaseError

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:

    def __init__(self, conf: AppConf) -> None:
        self._engine = create_engine(conf.db_url, echo=True)
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
    def session(self, session: Session = None) -> Callable[..., AbstractContextManager[Session]]:
        if session is not None:
            # user has to handle session themselve
            yield session

        session: Session = self._session_factory()
        print('create new session')
        try:
            yield session
        except Exception as e:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise DatabaseError(error_details=e)
        finally:
            session.close()
