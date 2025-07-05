from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat import GigaChat
import streamlit as st

def det_user_level(giga) -> str:
    level_prompt = """Твоя задача определить уровень знаний пользователя. Ты должен проанализировать ответ пользователя и дать ОДИН ОТВЕТ В ОДНО СЛОВО! Вот два варианта и критерии для каждого из них:
    1. "Новичок" - если пользователь говорит что не имеет большого опыта и не уверен в своих знаниях
    2. "Профи" - если пользователь говорит что опытен и разбирается в теме
    """
    
    messages = [SystemMessage(content=level_prompt)]
    
    user_input = st.text_input('Опишите свой уровень знаний в NLP:')
    
    if not user_input:
        st.stop()  
    
    messages.append(HumanMessage(content=user_input))
    res = giga.invoke(messages)
    
    promts = {
        "Новичок": "Ты помощник для новичков, ты должен отвечать на вопросы максимально понятно, поясняя сложные термины, избегать больших формул и пытаться приводить аналогии",
        "Профи": "Ты помощник для профессионалов, ты можешь использовать сложные термины без длинных пояснений, используй математические формулы для точного ответа"
    }
    
    return promts[res.content]