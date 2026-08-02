class ConversationHistory:

    async def add_user_message(self, session_id: str, content: str):
        pass

    async def add_assistant_message(self, session_id: str, content: str):
        pass

    async def get_messages(self, session_id: str):
        return []

    async def clear(self, session_id: str):
        pass