class SessionManager:

    async def create(self):
        pass

    async def exists(self, session_id: str):
        return True

    async def delete(self, session_id: str):
        pass

    async def list(self):
        return []

    async def rename(
        self,
        session_id: str,
        title: str
    ):
        pass