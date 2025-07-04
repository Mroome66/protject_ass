
from langchain_community.document_loaders import PyPDFLoader

class PDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
    
    def load_and_prepare_pdf(self) -> str:
        loader = PyPDFLoader(self.pdf_path)
        pages = loader.load()
        text = "\n".join([page.page_content for page in pages])
        promt = f"""
            Ты должен отвечать ТОЛЬКО на основе следующего документа:
            {text}
            Правила:
            1. Если вопрос не относится к теме документа: "Это вне рамок предоставленных материалов"
            2. Если требуется отвечать максимально понятно, то ты можешь пояснять термины развёрнуто.
            3. Не придумывай информацию, которой нет в документе.
            4. Для сложных вопросов объединяй информацию из разных частей документа
            """
        return promt