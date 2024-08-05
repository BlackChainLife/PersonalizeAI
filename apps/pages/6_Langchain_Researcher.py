from dotenv import load_dotenv
from gpt_researcher import GPTResearcher
import streamlit as st
import os
import asyncio
import socks
import socket
from apps.config import ROOT_PATH

from apps.service.utils import write_text_to_md

# 设置代理
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10793)
socket.socket = socks.socksocket


# 加载环境变量
load_dotenv()

def get_report_list():
    file_list = os.listdir(os.path.join(ROOT_PATH, "outputs"))
    file_path = [os.path.join(ROOT_PATH, key ) for key in file_list]
    return zip(file_list, file_path)

async def researcher(query):
    """
    This is a sample script that shows how to run a research report.
    """
    # Report Type
    report_type = "research_report"

    # Initialize the researcher
    researcher = GPTResearcher(query=query, report_type=report_type, config_path=None)
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    report = await researcher.write_report()
    
    return report


with st.sidebar:
    st.title("设置")
    st.checkbox("自动保存结果到文件", value=True)
    report_type = st.radio("生成报告类型", 
            ["简单报告", "深度调研报告", "Agent"], 
            captions=[
                "Summary - Short and fast (~2 min)",
                "Detailed - In depth and longer (~5 min)",
                "Detailed - Agent Assistant"
            ])

st.title("🔎 GPT-researcher 根据主题获取详细的调研报告")

tab1, tab2 = st.tabs(["生成调研报告", "历史调研报告"])

# 设置研究的子主题

if "subtopic" not in st.session_state:
    st.session_state["subtopic"] = []

with tab1:
    researcer_text = st.text_input("请输入需要调研的主题")

    col1, col2, col3 = st.columns([0.8, 0.1, 0.1], vertical_alignment="bottom")
    topic = col1.text_input("请输入子话题")
    if col2.button("添加"):
        if not topic:
            st.warning("子话题不能为空")
            st.stop()
        st.session_state.subtopic.append(topic)
        if st.session_state.subtopic:
            st.text_area("子话题", "\n".join(st.session_state.subtopic), 
                         label_visibility="hidden")
            
    if col3.button("开始") and researcer_text:
        async def run_research():
            result = await researcher(researcer_text)
            await write_text_to_md(result, researcer_text)
            st.markdown(result)
            
        asyncio.run(run_research())              

with tab2:
    history_report = st.selectbox("查看历史报告", get_report_list())
    path = os.path.join(ROOT_PATH, 'outputs', str(history_report) if history_report else "不存在")
    with st.container():
        with open(path) as f:
            st.markdown(f.read())
    















