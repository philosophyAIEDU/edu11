import streamlit as st
import openai
import time
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="필로소피 AI EDU 교육팀", page_icon="🎓")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_client" not in st.session_state:
    st.session_state.openai_client = None

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# 제목 표시
st.title("필로소피 AI EDU 교육팀 💬")

# API 키 입력
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요:", type="password")

if api_key:
    # OpenAI 클라이언트 설정
    if st.session_state.openai_client is None:
        st.session_state.openai_client = OpenAI(api_key=api_key)
        # 새로운 스레드 생성
        thread = st.session_state.openai_client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요.")

    # 메시지 처리
    if user_input:
        # 사용자 메시지를 스레드에 추가
        st.session_state.openai_client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_input
        )

        # Assistant를 실행
        run = st.session_state.openai_client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id="asst_SUFLgDjlRMn25ac2fZHphE0W"
        )

        # 실행 완료 대기
        while run.status != "completed":
            time.sleep(1)
            run = st.session_state.openai_client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )

        # 메시지 가져오기
        messages = st.session_state.openai_client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # 채팅 히스토리 표시
        for msg in reversed(messages.data):
            role = "assistant" if msg.role == "assistant" else "user"
            with st.chat_message(role):
                st.write(msg.content[0].text.value)

else:
    st.warning("OpenAI API 키를 입력해주세요.")
