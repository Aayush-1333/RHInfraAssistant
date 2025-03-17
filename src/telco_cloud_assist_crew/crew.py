from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from telco_cloud_assist_crew.tools.custom_tool import retrieve_chunks
from dotenv import load_dotenv
import os


load_dotenv()
HOST = os.environ['HOST']
API_KEY = os.environ['API_KEY']

vllm_model = LLM(
	model="hosted_vllm/meta-llama/Llama-3.2-3B-Instruct",
	temperature=0,
	max_tokens=12000,
	max_completion_tokens=6000,
	base_url=f'http://{HOST}:8200/v1',
	api_key=API_KEY
)


@CrewBase
class TelcoCloudAssistCrew():
	"""TelcoCloudAssistCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def planner(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
			verbose=True,
			llm=vllm_model,
			max_iter=3
		)

	@agent
	def designer(self) -> Agent:
		return Agent(
			config=self.agents_config['designer'],
			verbose=True,
			llm=vllm_model,
			max_iter=3
		)
	
	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			verbose=True,
			llm=vllm_model,
			max_iter=3
		)

	@task
	def plan_task(self) -> Task:
		return Task(
			config=self.tasks_config['plan_task'],
		)

	@task
	def design_task(self) -> Task:
		return Task(
			config=self.tasks_config['design_task'],
			tools=[retrieve_chunks]
		)
	
	@task
	def write_task(self) -> Task:
		return Task(
			config=self.tasks_config['write_task'],
			output_file="report.doc"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TelcoCloudAssistCrew crew"""

		return Crew(
			agents=self.agents, 
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
