# import streamlit as st


# def main():
#     st.header("言界-英语智能学习助手")

# if __name__ == '__main__':
#     main()

import streamlit as st
import os

# LLM model
os.system(f'git clone https://code.openxlab.org.cn/Alannikos/yanjie_1_8b.git ./LLM/model/')
os.system(f'cd ./LLM/model/ && git lfs pull')

# TTS model
os.system(f'git lfs install')
os.system(f'git clone https://hf-mirror.com/2Noise/ChatTTS ./TTS/weights/ChatTTS')

# ASR model
os.system(f'git lfs install')
os.system(f'git clone https://hf-mirror.com/FunAudioLLM/SenseVoiceSmall ./ASR/SenseVoiceSmall/')



def main():
    # 页面标题
    st.title("言界-英语智能学习助手")

    # 项目目标部分
    st.header("🔥 项目目标")
    st.write("提供情景对话和话题讨论，增强用户的口语交流能力。")
    st.write("通过视频对话，提升用户的真实体验和提高英语水平。")
    st.write("结合AI技术，提供个性化的伴读和伴写服务。")

    # 主要功能部分
    st.header("🌟 主要功能")
    with st.expander("展开查看详细功能"):
        st.write("- 普通对话：支持日常语音对话。")
        st.write("- 情境对话：利用场景引导大模型进行相关主题对话，模拟真实场景。")
        st.write("- 视频通话：结合数字人技术，提供更自然的交流体验。")

    # 项目实施计划路线
    st.header("🔄 项目实施计划路线")
    st.write("- 普通对话")
    st.write("- 情境对话")
    st.write("- 视频通话")
    st.write("- 探索中...")


    # 主要技术路线
    st.header("🚀 主要技术路线")
    with st.expander("展开查看技术详情"):
        st.write("- 多模态大语言模型")
        st.write("- TTS语音合成技术")
        st.write("- ASR语音识别技术")
        st.write("- Xtuner微调")
        st.write("- LMDeploy推理加速")
        st.write("- OpenXlab部署Demo")

    # 致谢部分
    st.header("💕 致谢")
    st.write("上海人工智能实验室")
    st.write("InternLM")
    st.write("xtuner")
    st.write("LMDeploy")

    # 添加一些样式和布局以提升界面美观度
    st.markdown("<style>body {background-color: #f2f3f4;}</style>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
