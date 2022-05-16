from app.core.conf import AppConf
from app.core.repository import AppRepository

class MyApp(object):
    def __init__(self, conf: AppConf, repo: AppRepository) -> None:
        self.conf = conf
        self.repo = repo
