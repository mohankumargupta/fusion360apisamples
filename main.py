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

What I need is python code samples in Fusion 360 api documentation website, 
but only in one category called Sketches.

This is a 2-step process.

**First step**

First task I need you to do is retrieve code sample names and urls under the Section called Sketches.

Here is where you get them

- Go to https://help.autodesk.com/view/fusion360/ENU/?guid=SampleList
- In the main content area of page, 
  Each link under the heading 'Sketches' (not Design:Sketch)

For step1, need to construct a list of {sample_name, sample_url, sample_code=null} 
sample_code is null in step1, it will be filled in step2. 

**Second step**
Now I need you to go each sample url in step1 and collect sample code for each, so step2  
fills in the sample_code entry in step1.

Here is how to get a single code sample.

1. Open a new tab
2. Go to sample_url.
3. make sure Python tab is selected.
4. extract sample code and put in sample_code
5. close tab

Please make sure that you only visit a link once. Do not visit  a link you have already visited.

The final output will be a json object which looks like this:
{
 'step1': <result of step1>
 'step2': <result of step2>
}


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
	history.save_to_file("history.json")

	with open("results.txt", "w", encoding="utf-8") as f:
		for i in h:
			content = i.result[-1].extracted_content
			if content:
				f.write(content)
	with open('final_results.txt', "w", encoding="utf-8") as f2:
	  f2.write(final_result)
    
if __name__ == '__main__':
	asyncio.run(run_search())