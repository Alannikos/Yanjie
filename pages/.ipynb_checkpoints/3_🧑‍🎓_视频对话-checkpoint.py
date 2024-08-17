# isort: skip_file
import sys
sys.path.append("/root/Yanjie")

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

    st.title('言界 - 英语智能学习助手')
    st.text("正在调优中...")

if __name__ == '__main__':
    main()