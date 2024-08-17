import io
import re
import numpy as np
import soundfile as sf
from pathlib import Path
import streamlit as st
from pydub import AudioSegment
from datetime import datetime
from ASR.FunASR.funasr import AutoModel
from audio_recorder_streamlit import audio_recorder

model_dir = "../SenseVoiceSmall"

def asr_show_audio(wav_path, sample_rate=24000):
    if wav_path is None:
        return
    # 读入音频
    # wav, sr = sf.read(wav_path, format='wav')
    
    # st.audio(wav, format="audio/wav", sample_rate=sample_rate)
    st.audio(wav_path, format="wav")

def save_wavs(wav_bytes):
    save_file = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".wav"
    wav_save_path = str(Path("../../Work_dirs/ASR").joinpath(save_file).absolute())
    
    audio_segment = AudioSegment.from_wav(io.BytesIO(wav_bytes))
    audio_segment.export(wav_save_path, format='wav')
    # wav_bytes.export(wav_save_path, format="wav")

    return wav_save_path

@st.cache_resource
def load_asr_model():
    model = AutoModel(model=model_dir,
                    vad_model="fsmn-vad",
                    vad_kwargs={"max_single_segment_time": 30000},
                    trust_remote_code=True, device="cuda:0")

    return model

# 调用模型生成文字
def audio2text(model, wav_path):
    texts = model.generate(
                        input=wav_path,
                        cache={},
                        language="auto", # "zn", "en", "yue", "ja", "ko", "nospeech"
                        use_itn=False,
                        batch_size_s=0,
    )

    new_text = re.sub("<.*?>", "", texts[0]["text"])
    return new_text


