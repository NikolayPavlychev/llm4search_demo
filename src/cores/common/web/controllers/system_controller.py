from classy_fastapi import Routable, get


class SystemController(Routable):
    def __init__(self, config_file: str):
        super().__init__()
        self.__config_file = config_file

    @get("/info")
    async def info(self):
        return {"config_file": self.__config_file, "version": "0.0.1"}
