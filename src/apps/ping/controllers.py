class PingController:
    @staticmethod
    def ping() -> str:
        return "pong!"


ping_controller = PingController()
