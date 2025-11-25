# Python 3.11.9
# pip install langchain-core==0.2.41 langchain==0.2.16 langchain-openai==0.1.23
# pip install langchain-openai>=0.2.0
# Streamlit을 사용하여 Python 파일을 실행하는 명령어
# streamlit run c:/Lecture/memory.py

import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.memory import ConversationBufferMemory



# 환경 변수 로드 (.env 파일에서 OPENAI_API_KEY 불러옴)
load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)


# 요약 저장 디렉토리 생성
SUMMARY_DIR = "summaries"
os.makedirs(SUMMARY_DIR, exist_ok=True)


# Streamlit UI 설정
st.set_page_config(page_title="요약 기반 기억 챗봇")
st.title("요약 기반 기억 챗봇")


# 사용자 식별자(thread_id)
thread_id = st.text_input("사용자 ID를 입력하세요:", value="default_user")
summary_path = os.path.join(SUMMARY_DIR, f"{thread_id}.txt")


# 사용자의 이전 대화 목록들이 요약되어 텍스트 파일로 저장됨
# 새로운 대화를 시작할 때 이전 요약을 불러와서 컨텍스트 유지
# 처음 접속한 사용자인 경우 빈 문자열로 시작
if os.path.exists(summary_path):
    with open(summary_path, "r", encoding="utf-8") as f:
        longterm_summary = f.read().strip()
else:
    longterm_summary = ""

# print(f"Long-term summary loaded: {longterm_summary}")   
 

# ConversationBufferMemory를 Streamlit 세션 상태로 관리
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

memory = st.session_state.memory


# LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

# LCEL 기반 프롬프트
main_prompt = PromptTemplate.from_template(
    """
    너는 사용자의 과거 요약 기억과 최근 대화를 참고해 대화하는 AI입니다.

    [이전 요약된 기억]
    {longterm_summary}

    [최근 대화]
    {history}

    [사용자 질문]
    {input}

    위 내용을 참고해서 자연스럽고 일관된 답변을 해주세요.
    """
)

# LCEL 체인 (Runnable 구성)
def get_chain(memory_obj, longterm_summary):
    return (
        {
            "input": RunnablePassthrough(),
            "history": RunnableLambda(lambda x: memory_obj.load_memory_variables({}).get("history", "")),
            "longterm_summary": RunnableLambda(lambda x: longterm_summary)
        }
        | main_prompt
        | llm
    )

conversation_chain = get_chain(memory, longterm_summary)

# 사용자 질문 입력 (엔터로 제출 가능)
question = st.text_input("질문을 입력하세요:")

# 버튼 추가: 사용자가 버튼을 눌러야만 답변 생성
submit_button = st.button("답변 생성")

if submit_button and question.strip() != "":
    with st.spinner("답변 생성 중..."):
        result = conversation_chain.invoke(question)
        answer = result.content
        st.write("### 답변:")
        st.write(answer)

        # 메모리에 대화 저장
        memory.save_context({"input": question}, {"output": answer})

        # ------------------------------
        # 요약 업데이트
        # ------------------------------
        summarizer_prompt = PromptTemplate.from_template(
            """
            다음은 최근 대화 내용입니다.
            이를 참고해서 전체 요약을 갱신해주세요.

            [이전 요약]
            {old_summary}

            [새로운 대화]
            {recent_chat}

            새로운 통합 요약:
            """
        )

        # 최근 대화내용을 저장할 빈 문자열 초기화 
        # 최근 6개의 대화 메시지를 "역할: 내용" 형태로 포맷팅하여 출력합니다.
        recent_chat = ""
        for msg in memory.chat_memory.messages[-6:]:
            role = "사용자" if msg.type == "human" else "AI"
            recent_chat += f"{role}: {msg.content}\n"


        summary_input = summarizer_prompt.format(
            old_summary=longterm_summary or "이전 요약 없음",
            recent_chat=recent_chat
        )

        summary_result = llm.invoke(summary_input)
        new_summary = summary_result.content.strip()

        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(new_summary)

        st.write("---")
        st.write("**요약된 기억(장기기억):**")
        st.write(new_summary)


# 최근 10개의 대화 메시지를 "역할: 내용" 형태로 포맷팅하여 출력합니다.
if memory.chat_memory.messages:
    st.write("---")
    st.write("**최근 대화 기록:**")
    for msg in memory.chat_memory.messages[-10:]:
        role = "사용자" if msg.type == "human" else "AI"
        st.write(f"{role}: {msg.content}")

