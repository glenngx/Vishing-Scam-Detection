import torch
import torchaudio
import soundfile as sf
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from pyctcdecode import build_ctcdecoder, Alphabet
from io import BytesIO

def load_speech_to_text_model():
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
    labels = processor.tokenizer.convert_ids_to_tokens(range(len(processor.tokenizer)))
    alphabet = Alphabet.build_alphabet(labels)
    decoder = build_ctcdecoder(labels, kenlm_model_path=None)
    return processor, model, decoder

def wav_to_text(file_bytes, processor, model, decoder):
    try:
        waveform, sample_rate = sf.read(BytesIO(file_bytes))
        print(f"Original waveform shape: {waveform.shape}, Sample rate: {sample_rate}")

        if len(waveform.shape) > 1 and waveform.shape[1] > 1:
            waveform = np.mean(waveform, axis=1)
            print(f"Converted to mono: {waveform.shape}")

        if sample_rate != 16000:
            waveform = torchaudio.functional.resample(torch.tensor(waveform).float(), sample_rate, 16000).numpy()
            print(f"Resampled waveform shape: {waveform.shape}, Sample rate: 16000")

        min_length = 16000 * 5  # Minimum length of 5 seconds at 16000 Hz
        if waveform.shape[0] < min_length:
            padding = min_length - waveform.shape[0]
            waveform = np.pad(waveform, (0, padding), 'constant')
        print(f"Processed waveform shape: {waveform.shape}")

        window_length = 16000 * 5  # 5-second window
        stride = 16000 * 2  # 2-second stride
        transcriptions = []

        for start in range(0, len(waveform) - window_length + 1, stride):
            window = waveform[start:start + window_length]
            input_values = processor(window, return_tensors="pt", sampling_rate=16000).input_values
            with torch.no_grad():
                logits = model(input_values).logits
            transcription = decoder.decode(logits.numpy()[0])
            transcriptions.append(transcription)

        full_transcription = " ".join(transcriptions)
        return full_transcription

    except Exception as e:
        print(f"Error in wav_to_text: {str(e)}")
        return "Error: Could not process the audio file. Please ensure it's a valid WAV file."
