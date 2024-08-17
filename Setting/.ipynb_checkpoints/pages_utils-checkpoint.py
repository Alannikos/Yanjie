import streamlit as st
from audio_recorder_streamlit import audio_recorder

def init_sidebar():
    with st.sidebar:
        with st.container():
            st.write("此处放置不同应用")  
        with st.container():
            tab1, tab2, tab3 = st.tabs(["ASR设置", "TTS设置", "LLM设置"])

            with tab1:
                # audio_bytes = audio_recorder()
                audio_bytes = audio_recorder(
                    text="",
                    recording_color="#e8b62c",
                    neutral_color="#6aa36f",
                    icon_name="microphone",
                    icon_size="6x",
                )
                if audio_bytes:  # 如果获取到了声音
                    st.write("录制成功")

            with tab2:
                # TTS_Check_Radio会接受到用户选择
                TTS_Check_Radio = st.radio(
                    "是否开启语音聊天",
                    ("是", "否")
                )

            with tab3:
                LLM_Option_Radio = st.radio(
                    "请选择大语言模型",
                    ("InternLM", "Qwen")
                )    

if __name__ == "__main__":
    init_sidebar()