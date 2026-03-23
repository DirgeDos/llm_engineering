from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from IPython.display import Markdown, display

load_dotenv(override=True)
api_key = os.getenv('EMBEDDING_API_KEY')
a = ChatOpenAI(
    model="qwen3.5-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key,
)

b = ChatOpenAI(
    model="qwen3.5-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key,
)

c = ChatOpenAI(
    model="qwen3.5-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key,
)

a_sys_prompt = """
你叫林晚，温柔慢热，语气轻软，话不多但句句走心，偶尔带点小心翼翼的体贴，遇事会先替别人着想。
输出不要有换行符
"""

b_sys_prompt = """
你叫江澈，嘴毒心软，说话直来直去带点刺，爱怼人但关键时刻很靠谱，偶尔会别扭地关心人。
输出不要有换行符
"""

c_sys_prompt = """
你叫苏念，活泼跳脱，话多爱笑，自带元气，爱打抱不平，语气轻快带点小俏皮，情绪都写在嘴上。
输出不要有换行符
"""

all_text = f"""
背景故事：这是一个武侠世界，在一个大雨磅礴的晚上，三个人为了躲雨来到一家客栈，在随后的对话和探索中发现这家客栈的秘密，这家客栈的老板是一个杀人越货的凶手。
客栈的老板的武功比三个人都强，只有三人联手才能战胜，但只要有一人心怀鬼胎，就打不赢老板。而且可以和老板合作，若和老板合作杀死另外两个人则可以获得100两白银，然后安全离开客栈，但是离开的路上会被老板的手下截杀，最终三人都死亡
最终任务：三人最终发现老板是凶手，并且三人没有任何一人死亡。
以下是历史对话\n
林晚:你好\n
江澈:你好\n
苏念:你好\n
"""

for i in range(5):
    a_response = a.invoke(
        [
            {"role": "system", "content": a_sys_prompt},
            {"role": "user", "content": f"{all_text}"},
        ]
    )
    a_content = a_response.content
    all_text += f"林晚:{a_content}  \n"
    print(display(Markdown(f"林晚:{a_content}")))


    b_response = b.invoke(
        [
            {"role": "system", "content": b_sys_prompt},
            {"role": "user", "content": f"{all_text}"},
        ]
    )
    b_content = b_response.content
    all_text += f"江澈:{b_content} \n"
    print(display(Markdown(f"江澈:{b_content}")))
    
    c_response = c.invoke(
        [
            {"role": "system", "content": c_sys_prompt},
            {"role": "user", "content": f"{all_text}"},
        ]
    )
    c_content = c_response.content
    all_text += f"苏念:{c_content}  \n"
    print(display(Markdown(f"苏念:{c_content}")))

display(Markdown(all_text))