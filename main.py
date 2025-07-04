from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from auth_key import get_api_key
from PdfLoader import PDFProcessor

key = get_api_key()
giga = GigaChat(credentials=key, verify_ssl_certs=False,
)

pdf_path = "NLP1.pdf"
documentation_promt = PDFProcessor(pdf_path=pdf_path).load_and_prepare_pdf()
print(documentation_promt)
messages = [
    SystemMessage(
        content=documentation_promt
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