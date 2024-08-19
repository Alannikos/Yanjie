import sys
import os
sys.path.append("./TTS")

# ==================================================================
#                             第三方库导入配置
# ==================================================================
import torch
import torchaudio
import numpy as np
from model.ChatTTS import ChatTTS  # chattts仓库
import soundfile as sf  # 音频文件读入与存储
from pathlib import Path
from datetime import datetime  # 后面需要生成文件名
import streamlit as st  # 界面部分

from IPython.display import Audio  # 测试音频是否正确

# 这里可以做成一个init
chat = ChatTTS.Chat()
chat.load(compile=False, source='custom', custom_path='./TTS/weights/ChatTTS')  # 用这个最新的配置

# 模型侧边栏选择
def prepare_tts_generation_config():
    model_type = st.selectbox("助手音色", key="config_voice_model_type", options=["温柔御姐", "可爱甜心"])

    if model_type == "温柔御姐":
        return "./TTS/weights/speaker/seed_742_restored_emb.pt"
    else:
        return "./TTS/weights/speaker/seed_1089_restored_emb.pt"

# 展示音频文件
def show_audio(wav_save_path, sample_rate = 24000):
    if wav_save_path is None:
        return
    # 读入音频
    st.audio(wav_save_path, format="audio/wav")

# 保存音频文件
def save_wavs(wav, wav_save_path):
    """
    参数说明：\n
        1. wav: 声音文件
        2. wav_save_path: 音频文件保存地址

    """
    wav_data = np.array(wav[0])
    sf.write(wav_save_path, wav_data, samplerate=24000)

# 文本转语音
def text2audio(text, speaker_type=None, oral=3, laugh=3, bk=3):
    """
    参数说明：\n
        1. text: 文本\n
        2. oral: 口语\n
        3. laugh: 笑声\n
        4. bk: 停顿\n
        5. wav_save_path: 音频文件保存地址
    """
    if speaker_type == None:
        speaker = chat._encode_spk_emb(torch.load('./TTS/weights/speaker/seed_1089_restored_emb.pt'))
    else:
        speaker = chat._encode_spk_emb(torch.load(speaker_type))

    # 句子全局设置：讲话人音色和速度
    params_infer_code = ChatTTS.Chat.InferCodeParams(
        spk_emb=speaker, # 声音模型
    )

    """
    句子全局设置：口语连接、笑声、停顿程度
    params_refine_text = ChatTTS.Chat.RefineTextParams(
        prompt='[oral_{}][laugh_{}][break_{}]'.format(oral, laugh, bk),
    )
    """
    
    """
    得到音频文件
    type: list[array()]
    """
    wavs = chat.infer(
        text,
        # params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )
    save_file = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".wav"
    wav_save_path = str(Path("./Work_dirs/TTS").joinpath(save_file).absolute())
    save_wavs(wavs, wav_save_path)
    
    return wav_save_path

# 模型测试
def test(model_text):
    text2audio(
        model_text,
    )


if __name__ == "__main__":
    text = ["哈哈哈，你知道我是谁吗"]
    test(text)