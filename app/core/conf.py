class AppConf(object):
    def __init__(self, conf):
        self.db_url = conf["db_url"]
        self.jwt_secret: str = conf["jwt_secret"]

    def __repr__(self) -> str:
        return '<Config db_url={} jwt_secret={}>'.format(self.db_url, self.jwt_secret)
