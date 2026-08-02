class TextSynthException(Exception):
    pass


class DocumentNotFound(TextSynthException):
    pass


class SessionNotFound(TextSynthException):
    pass


class InvalidDocument(TextSynthException):
    pass


class VectorStoreError(TextSynthException):
    pass


class LLMError(TextSynthException):
    pass