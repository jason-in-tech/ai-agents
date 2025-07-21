from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

class TrendingCompany(BaseModel):
    """ A company that is in the news and attracting attention """
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """ List of multiple trending companies that are in the news """
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """ Detailed research on a company """
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        # want trending company finder to have memory such that it won't search for the same company twice
        return Agent(config=self.agents_config['trending_company_finder'],
                     tools=[SerperDevTool()], memory=True)
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], 
                     tools=[SerperDevTool()])

    @agent
    def stock_picker(self) -> Agent:
        # want stock picker to have memory such that it won't recommend the same stock twice
        return Agent(config=self.agents_config['stock_picker'], 
                     tools=[PushNotificationTool()], memory=True)
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'],
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""
        # manager agent is used to manage the crew
        # it is not defined as @agent, so it is not a crew member
        # it is used to manage the crew and not do the work
        manager = Agent(
            config=self.agents_config['manager'],
            # allow the manager agent to delegate tasks to the crew members
            # this is equivalent to the handoffs in the sales agent example (in Openai SDK)
            allow_delegation=True
        )
            
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            # we are using a manager agent to figure out which agent does which task
            process=Process.hierarchical,
            verbose=True,
            # pass the manager agent to the crew
            manager_agent=manager,
            # turn memory on
            memory=True,
            # Long-term memory for persistent storage across sessions
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            # Short-term memory for current context using RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small'
                            }
                        },
                        type="short_term",
                        path="./memory/"
                    )
                ),            
            # Entity memory for tracking key information about entities
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )
