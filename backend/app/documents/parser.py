from pathlib import Path

from app.documents.factory import LoaderFactory


class DocumentParser:
    """
    Parser principal de documentos.

    Su única responsabilidad es delegar el trabajo
    al loader correspondiente según la extensión.
    """

    def __init__(self):

        self.factory = LoaderFactory()

    # ---------------------------------------------------------

    def parse(self, file_path: str | Path):

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(file_path)

        loader = self.factory.get_loader(file_path)

        return loader.load(file_path)