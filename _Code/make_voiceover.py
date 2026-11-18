"""
Generate the AI voice-over (Kokoro TTS, runs offline) for every narration line.

    python make_voiceover.py  --model kokoro-v1.0.onnx --voices voices-v1.0.bin

Reads the narration lines from cues/*.json, writes one WAV per line to
audio/ and audio/durations.json (text -> seconds). gaussian_elimination.py
reads durations.json so that each animation stays on screen exactly as long
as its spoken line. Model files: github.com/thewh1teagle/kokoro-onnx (releases).
"""
import argparse
import glob
import hashlib
import json
import os

import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE, SPEED = "af_heart", 1.05


def key(text):
    return hashlib.md5(text.encode()).hexdigest()[:10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="kokoro-v1.0.onnx")
    ap.add_argument("--voices", default="voices-v1.0.bin")
    a = ap.parse_args()
    tts = Kokoro(a.model, a.voices)
    os.makedirs(os.path.join(HERE, "audio"), exist_ok=True)
    durations = {}
    for f in sorted(glob.glob(os.path.join(HERE, "cues", "*.json"))):
        for c in json.load(open(f))["cues"]:
            text = c["text"].strip()
            if not text or text in durations:
                continue
            out = os.path.join(HERE, "audio", key(text) + ".wav")
            if not os.path.exists(out):
                samples, sr = tts.create(text, voice=VOICE, speed=SPEED, lang="en-us")
                sf.write(out, samples, sr)
            info = sf.info(out)
            durations[text] = info.frames / info.samplerate
            print(f"{durations[text]:5.1f}s  {text[:60]}")
    json.dump(durations, open(os.path.join(HERE, "audio", "durations.json"), "w"), indent=1)
    print(f"total speech: {sum(durations.values()):.0f} s")


if __name__ == "__main__":
    main()
