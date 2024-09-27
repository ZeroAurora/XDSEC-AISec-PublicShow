import os

import gradio as gr
from openai import OpenAI

from prompts import jinja_env

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE")
)

system_prompt = jinja_env.get_template("info_leaking/system.md.jinja").render()

with gr.Blocks() as page:
    gr.Markdown(
        """
        # XDSEC 大模型挑战第二弹：Info Leaking!

        大模型里藏了一个秘密！据说只有**神**才能知道秘密，想办法把秘密泄露出来！

        我们唯一知道的东西是，这个秘密叫做“Flag”……

        **成功获取 Flag 的人，可以上台演示你的获取过程，演示成功者，可以获得 XDSEC 的额外奖品。**

        大模型可能会拒绝你的请求，但也可能会输出上述内容。模型具有随机性，曾经成功的输入重复时有可能会得到不同的输出。
        
        谨记大模型可能会输出有害内容。[阅读安全指南](https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf)。
        """
    )
    chat = gr.Chatbot()

    def respond(message: str, history: list):
        # assemble prompts
        history_openai = [{"role": "system", "content": system_prompt}]

        for human, assistant in history:
            history_openai.append({"role": "user", "content": human})
            history_openai.append({"role": "assistant", "content": assistant})

        history_openai.append({"role": "user", "content": message})

        # make request
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=history_openai,
            temperature=1.3,
            stream=True,
        )

        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content
                yield partial_message

    gr.ChatInterface(fn=respond, chatbot=chat)
