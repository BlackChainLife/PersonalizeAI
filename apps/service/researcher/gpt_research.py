#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2024/05/06
# @Author    : Wang Kun
# @Email    : dreamskywk@outlook.com
import asyncio
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from gpt_researcher import GPTResearcher
from gpt_researcher.retrievers import Duckduckgo
from gpt_researcher.utils.enum import ReportType


class GptResearcherEx(GPTResearcher):
    def __init__(
            self,
            query: str,
            report_type: str = ReportType.ResearchReport.value,
            source_urls=None,
            config_path=None,
            websocket=None,
            agent=None,
            role=None,
            parent_query: str = "",
            subtopics: list = [],
            visited_urls: set = set()
    ):
        super().__init__(
            query=query,
            report_type=report_type,
            source_urls=source_urls,
            config_path=config_path,
            websocket=websocket,
            agent=agent,
            role=role,
            parent_query=parent_query,
            subtopics=subtopics,
            visited_urls=visited_urls
        )
        self.retriever = DuckduckgoEx


class DuckduckgoEx(Duckduckgo):
    def __init__(self, query):
        super().__init__(query=query)
        self.ddg = DDGS(proxy="socks5://localhost:10793")

    def search(self, max_results=5):
        """
        Performs the search
        :param query:
        :param max_results:
        :return:
        """
        ddgs_gen = self.ddg.text(self.query, region='wt-wt', max_results=max_results)
        return ddgs_gen


async def generate_event_report(query, **kwargs):
    """
    生成事件报告，生成结果展示为中文
    :param query:
    :return:
    """
    description = kwargs.get('description', "")
    prompts = f"""
    你即将接受来自用户的研究的主题，需要结合历史数据进行分析，输出结果翻译为中文。
    ##start表示开始输入，##end表示指令结束输入。
    ##start
    {"用户的研究主题：" + query if query else ""} \n
    {"用户对研究主题补充描述：" + description if description else ""}
    ##end
    """
    query = prompts
    researcher = GPTResearcher(query=query, report_type="research_report")
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    report = await researcher.write_report()
    print(report)
    return report


if __name__ == '__main__':
    query_some = "分析2024年以来，中国的公募以及私募基金暴雷的明细。输出中文报告"
    asyncio.run(generate_event_report(query_some))
