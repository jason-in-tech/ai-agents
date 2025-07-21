from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task



@CrewBase
class Coder():
    """Coder crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # One click install for Docker Desktop:
    #https://docs.docker.com/desktop/

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'],
            verbose=True,
            # allow agent to execute code
            allow_code_execution=True,
            # ensures it runs within the docker container
            # and it's not running the code on the host machine
            code_execution_mode="safe",  # Uses Docker for safety
            # max execution time for the code
            # since it's a simple task, we can set it to 30 seconds
            max_execution_time=30, 
            # max retry limit for the code
            # since it's a simple task, we can set it to 3
            max_retry_limit=3 
    )


    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Coder crew"""


        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
