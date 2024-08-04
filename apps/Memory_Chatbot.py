import os
import socks
import socket
import streamlit as st

from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage,trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

from apps.service.get_config_openai import OPENAI_MODEL_LIST


# 加载环境变量
load_dotenv()

# 设置代理
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10793)
socket.socket = socks.socksocket

# 初始化openai 的可以
openai_api_key=os.getenv("OPENAI_API_KEY")
openai_base_url=os.getenv("OPENAI_BASE_URL")

# 设置初始化请求参数
llm_model = "gpt-3.5-turbo"
llm_system_message = "你是一个有用的机器人"

with st.sidebar:
    max_token = st.number_input('TOKEN数量限制', value=2048, min_value=1024, max_value=4096)
    temperature = st.number_input("temperature", value=0.1, min_value=0.1, max_value=2.0, step=0.1)
    top_p = st.number_input("top_p", value=0.8, min_value=0.1, max_value=1.0, step=0.1)
    choice_model =  st.selectbox("选择模型", OPENAI_MODEL_LIST)
    prompt_template = st.selectbox(
        "选择提示词",
        (1, 2),
        placeholder="请选择提示词"
    )
    
st.title("💬 Chat机器人")
st.caption("🚀 基于OpenAI开发的带有记忆的聊天机器人")

# st.button("新建对话")
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [SystemMessage(content="How can I help you?")]

for msg in st.session_state.messages:
    if isinstance(msg, (SystemMessage, AIMessage)):
        st.chat_message('assistant').write(msg.content)
    else:
        st.chat_message('user').write(msg.content)

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    llm = ChatOpenAI(
        model=choice_model or llm_model,
        temperature=temperature,
        max_tokens=int(max_token),
        timeout=300000,
        max_retries=2
    )
    
    prompt_load = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    
    trimmer = trim_messages(
        max_tokens=max_token,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )
    # 发起请求
    chain = (
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
        | prompt_load
        | llm
    )

    # 用户输入展示在界面上
    st.chat_message("user").write(prompt)
    # 发起请求
    request_params = {
        "messages": st.session_state["messages"] + [HumanMessage(content=prompt)], 
        "language": "Chinese"
    }
    st.session_state.messages.append(HumanMessage(content=prompt))
    response = chain.invoke(request_params)
    st.session_state.messages.append(AIMessage(content=response.content))
    st.chat_message("assistant").write(response.content)
