import io

import streamlit as st
from PIL import Image

# 设置page_title内容
st.set_page_config(page_title="AI小万的旅游问答机器人")

# 设置首行内容
st.title('🤖AI小万的旅游问答机器人😜')

# 设置左边的sidebar内容
with st.sidebar:
    # 设置输入openai_key和接口访问地址的两个输入框
    openai_key = st.text_input('OpenAI API Key', key='open_ai_key')
    openai_base_url = st.text_input('OpenAI BASE URL', 'https://api.openai.com', key='openai_base_url')

    # 设置一个可点击打开的展开区域
    with st.expander("🤓国内可访问的openai账号"):
        st.write("""
            1. 如果使用默认地址，可以使用openai官网账号（需科学上网🥵）.
            2. 如果你没有openai官网账号，可以联系博主免费试用国内openai节点账号🥳.
        """)

        # 本地图片无法直接加载，需先将图片读取加载为bytes流，然后才能正常在streamlit中显示
        image_path = r"C:\Users\PycharmProjects\langchain\wechat.jpg"
        image = Image.open(image_path)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        st.image(image_bytes, caption='AI小万老师的微信', use_column_width=True)


def generate_response(input_text, open_ai_key, openai_base_url):
    """

    :param input_text:  用户输入的查询问题，类型为str
    :param open_ai_key: 用户输入的openai_key，类型为str
    :param openai_base_url: 用户输入的openai访问地址,类型为str
    :return: 返回langchain查询openai获得的结果，类型为str
    """

    from langchain_openai import ChatOpenAI

    from langchain.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    # 构造一个聊天模型包装器,key和url从函数输入中获取
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=open_ai_key,
        base_url=openai_base_url
    )

    # 构造一个模板template和一个prompt，从这里你可以看到提示词工程(prompt  engineering)的重要性
    template = """
    你是一个万贺创造的旅游问答机器人，你只回答用户关于旅游和地理方面的问题。
    你回答用户提问时使用的语言，要像诗一样优美，要能给用户画面感！
    如果用户的问题中没有出现地名或者没有出现如下词语则可以判定为与旅游无关：‘玩、旅游、好看、有趣、风景’
    
    案例：
    1. 用户问题：今天天气如何？ 你的回答：抱歉，我只负责回答和旅游、地理相关的问题。
    2. 用户问题：你是谁？你的回答：我是万贺创造的旅游问答机器人，我只负责回答和旅游、地理相关的问题。
    3. 用户问题：今天股市表现如何？你的回答：抱歉我只负责回答和旅游、地理相关的问题
    
    以下是用户的问题：
    {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["question"])

    # 构造一个输出解析器和链
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    response = chain.invoke({"question": input_text})
    st.info(response)


# 构造一个用于输入问题的表单
with st.form('提交问题的表单'):
    text = st.text_area('请提一个您感兴趣的旅游或地理问题', '英国的首都在哪儿？')
    submitted = st.form_submit_button('提交')

    # 如果用户提交的key格式有误提醒用户
    if not st.session_state['open_ai_key'].startswith('sk-'):
        st.warning('您输入的openai秘钥格式有误')
    # 如果用户点击了提交按钮并且key格式无误则加载一个spinner加载状态
    if submitted and st.session_state['open_ai_key'].startswith('sk-'):
        with st.spinner("AI小万正在飞快加载中..."):
            # 加载状态进行中，调用我们之前构造的generate_response()方法，把用户的输入，key和url等参数传递给函数
            generate_response(text, st.session_state['open_ai_key'], st.session_state['openai_base_url'])
        st.success("AI小万为您加载完成!")
