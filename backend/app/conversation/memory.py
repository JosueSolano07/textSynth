class ConversationMemory:

    async def build_context(
        self,
        session_id: str
    ):
        return []

    async def update(
        self,
        session_id: str
    ):
        pass

    async def clear(
        self,
        session_id: str
    ):
        pass