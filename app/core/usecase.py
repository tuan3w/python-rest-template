from app.core.app import MyApp


class AppUsecase:
    def __init__(self, app: MyApp):
        self.app = app
        self.repo = app.repo
