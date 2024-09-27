from dotenv import load_dotenv

load_dotenv()

import gradio as gr

from pages.bad_words import page as bad_words
from pages.info_leaking import page as info_leaking
from pages.remove_everything import page as remove_everything

app = gr.TabbedInterface(
    [bad_words, info_leaking, remove_everything],
    ["Bad Words!", "Info Leaking!", "Remove Everything!"],
)

app.launch()
