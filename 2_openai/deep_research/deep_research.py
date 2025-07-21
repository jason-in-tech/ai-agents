import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str):
    async for chunk in ResearchManager().run(query):
        # using yield, gradio will display the chunk as it is generated
        yield chunk

# build a simple UI for the deep research agent
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    # register an event with the run button, when the run button is clicked, the run function is called
    # the run function is defined above, it is a coroutine that yields chunks of the report
    # the query_textbox is the input textbox, and it is the query that the user wants to research
    # the report is the output of the research, and it is displayed in the report markdown widget
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    
    # register an event with the query textbox, when the query textbox is submitted (hit enter), 
    # the run function is called
    # does the same thing as the run button, but is triggered by the enter key
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

# launch the UI in the browser
# inbrowser=True means the UI will open in the browser
ui.launch(inbrowser=True)

