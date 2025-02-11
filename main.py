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

What I need is python code samples under the section name "Sketchs"(not Design:Sketch).

This is a 2-step process.

**First step**

First task I need you to do is remember the code sample names and urls.

Here is where you get them

- Go to https://help.autodesk.com/view/fusion360/ENU/?guid=SampleList
- In the main content area of page, 
  Each link under the heading 'Sketches' (not Design:Sketch)

The final result for step 1 will be a json object with schema [{sample name, sample url}]

**Second step**
Now I need you to go the sample urls 1 by 1 in step1 and collect sample code for each. 


The final result for this step 2 will be a json object with schema [{sample name, sample url, sample code}]

"""

async def run_search():
	agent = Agent(
		task=(
			TASK
		),
		llm=llm,
		max_actions_per_step=4,
	)
	
	history = await agent.run(max_steps=250)
	h = history.history
	final_result = history.final_result()
	
	with open("results.txt", "w", encoding="utf-8") as f:
		for i in h:
			content = i.result[-1].extracted_content
			if content:
				f.write(content)
	with open('final_results.txt', "w", encoding="utf-8") as f2:
	  f2.write(final_result)
    
	#history.save_to_file("history.json")

if __name__ == '__main__':
	asyncio.run(run_search())