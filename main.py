import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


TASK = """
Go to https://help.autodesk.com/view/fusion360/ENU/?guid=SampleList
In the main content area of page, 
  For the first 2 links under the heading 'Sketches' (not Design:Sketch):
    1. Go to page
	2. Make sure python tab is selected.
	3. 
	  display verbatim "START CODESAMPLE"
      display the text "<name of sketch>.py"
      display the code sample. 
      display verbatim "END CODESAMPLE"
"""

async def run_search():
	agent = Agent(
		task=(
			TASK
		),
		llm=llm,
		max_actions_per_step=4,
	)
	
	history = await agent.run(max_steps=25)
	h = history.history
	#final_result = history.final_result()
	with open("final_results.txt", "w") as f:
		for i in len(h):
			content = h[i].result[-1].extracted_content
			f.write(content)


	#history.save_to_file("history.json")

if __name__ == '__main__':
	asyncio.run(run_search())