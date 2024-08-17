# isort: skip_file
import sys
sys.path.append("../")
import copy
import warnings
from datetime import datetime
from dataclasses import asdict, dataclass
from typing import Callable, List, Optional

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import torch
from torch import nn
from transformers.generation.utils import (LogitsProcessorList,
                                           StoppingCriteriaList)
from transformers.utils import logging
from transformers import AutoTokenizer, AutoModelForCausalLM  # isort: skip
logger = logging.get_logger(__name__)


from LLM.utils_llm import load_model, prepare_llm_generation_config, combine_history, generate_interactive
from LLM.utils_llm import get_avatar
from TTS.utils_tts import text2audio, show_audio, prepare_tts_generation_config
from ASR.utils_asr import save_wavs, audio2text, load_asr_model, asr_show_audio

def main():
    print("重新运行main函数")
    # torch.cuda.empty_cache()
    print('load model begin.')
    model, tokenizer = load_model()
    asr_model = load_asr_model()
    print('load model end.')


    st.title('言界 - 英语智能学习助手')

    # 两个模型的设置
    llm_generation_config = None
    tts_generation_config = None
    st.session_state.theme_selected = '无'

    # 侧边栏设置
    with st.sidebar:
        print("重新运行sidebar函数")
        tabs = st.tabs(["语言模型设置", "语音模型设置"])
        # 语言模型设置
        with tabs[0]:
            llm_generation_config = prepare_llm_generation_config()
        # 语音模型设置
        with tabs[1]:
            tts_generation_config = prepare_tts_generation_config()
            st.toggle("是否显示文字", key="config_show_text")
 
        # 显示进行语音聊天按钮
        cols = st.columns(3)
        with cols[1]:
            print("重新运行audio_recorder函数")
            audio_bytes = audio_recorder(
                text="",
                recording_color="#e8b62c",
                neutral_color="#6aa36f",
                icon_name="microphone",
                icon_size="3x",
                pause_threshold=2.5,
                sample_rate=24000
            )
        print("audio_bytes是否为空", audio_bytes == None)


    # 初始化对话记录
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 在应用重启后展示历史记录
    for message in st.session_state.messages:
        with st.chat_message(message['role'], avatar=get_avatar("person2" if message['role'] == 'user' else "person1")):
            st.markdown(message['content'])
            if 'wav_path' in message.keys():
                show_audio(message['wav_path'])

    # 接受用户文字输入
    if prompt := st.chat_input('You are welcome to chat with me, please enter your question:'):
        print("重新运行prompt函数")
        # if prompt:
        # 展示用户输入的问题
        with st.chat_message('user', avatar=get_avatar("person2")):
            st.markdown(prompt)
        real_prompt = combine_history(prompt)
        # 把用户输入加到历史记录中
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
        })

        with st.chat_message('robot', avatar=get_avatar("person1")):
            message_placeholder = st.empty()
            for cur_response in generate_interactive(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=real_prompt,
                    additional_eos_token_id=92542,
                    **asdict(llm_generation_config),
            ):
                # 展示模型输出的结果
                message_placeholder.markdown(cur_response)
            # message_placeholder.markdown(cur_response)
            with st.spinner():
                wav_path = text2audio(cur_response, speaker_type=tts_generation_config)
                show_audio(wav_path)
        # 把模型语音输出结果加到历史对话中
        st.session_state.messages.append({
            'role': 'robot',
            'content': cur_response,  # pylint: disable=undefined-loop-variable
            'wav_path': wav_path
        })
        torch.cuda.empty_cache()
    elif (audio_bytes != None):
        # 先对录音进行保存，然后转文字
        save_voice_path = save_wavs(audio_bytes)
        print("audio_bytes是否为空", audio_bytes == None)
        with st.spinner():
            voice_prompt = audio2text(asr_model, save_voice_path)

        if voice_prompt:
            with st.chat_message('user', avatar=get_avatar("person2")):
                # 展示用户输入的问题
                st.markdown(voice_prompt)
                # 展示用户的语音输入
                asr_show_audio(save_voice_path)
        
        real_prompt = combine_history(voice_prompt)
        # 把用户输入加到历史记录中
        st.session_state.messages.append({
            'role': 'user',
            'content': voice_prompt,
            'wav_path':save_voice_path
        })

        with st.chat_message('robot', avatar=get_avatar("person1")):
            message_placeholder = st.empty()
            for cur_response in generate_interactive(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=real_prompt,
                    additional_eos_token_id=92542,
                    **asdict(llm_generation_config),
            ):
                # 展示模型输出的结果
                message_placeholder.markdown(cur_response)
            # message_placeholder.markdown(cur_response)
            with st.spinner():
                wav_path = text2audio(cur_response, speaker_type=tts_generation_config)
                show_audio(wav_path)
        # 把模型语音输出结果加到历史对话中
        st.session_state.messages.append({
            'role': 'robot',
            'content': cur_response,  # pylint: disable=undefined-loop-variable
            'wav_path': wav_path
        })
        torch.cuda.empty_cache()
    else:
        print("重新运行pass函数")
        pass

    print("============={}===============".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))

if __name__ == '__main__':
    main()