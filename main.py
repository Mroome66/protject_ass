from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from auth_key import get_api_key
from PdfLoader import PDFProcessor
from analysis_level import det_user_level

key = get_api_key()
giga = GigaChat(credentials=key, verify_ssl_certs=False,
)
level_promt = det_user_level(giga)
pdf_path = "NLP1.pdf"
documentation_promt = PDFProcessor(pdf_path=pdf_path).load_and_prepare_pdf()

messages = [
    SystemMessage(
        content=f"{level_promt}\n {documentation_promt}"
    )
]

while(True):
    user_input = input("Пользователь: ")
    if user_input == "пока":
      break
    messages.append(HumanMessage(content=user_input))
    res = giga.invoke(messages)
    messages.append(res)
    print("GigaChat: ", res.content)