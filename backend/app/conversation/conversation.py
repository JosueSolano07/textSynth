class ConversationManager:

    async def load(self, session_id: str):
        pass

    async def save(self, session_id: str):
        pass

    async def append_user_message(
        self,
        session_id: str,
        content: str
    ):
        pass

    async def append_assistant_message(
        self,
        session_id: str,
        content: str
    ):
        pass

    async def get_context(
        self,
        session_id: str
    ):
        pass