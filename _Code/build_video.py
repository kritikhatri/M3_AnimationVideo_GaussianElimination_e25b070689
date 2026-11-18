"""
Join the six rendered scenes into one MP4 and write the narration script.

    python build_video.py                      # silent video + script + subtitles
    python build_video.py --voice narration.m4a  # use your own recorded voice-over instead
    python build_video.py --silent               # no audio at all

By default the AI voice-over lines in audio/ (made by make_voiceover.py) are
placed at the start time of their narration cue and mixed into one track.

Outputs (in the repository root, one level up):
    _Video.mp4            final video (1080p, 30 fps, H.264)
    Narration_Script.md   what to say, with start/end times for every line
    narration.srt         same lines as subtitles (handy as a teleprompter)
"""
import json
import os
import subprocess
import sys

SCENES = ["S1_Hook", "S2_Concept", "S3_Intuition", "S4_Example",
          "S5_Interpretation", "S6_Summary"]
TITLES = {"S1_Hook": "Scene 1 - Hook / Context",
          "S2_Concept": "Scene 2 - Concept Introduction",
          "S3_Intuition": "Scene 3 - Visual Intuition",
          "S4_Example": "Scene 4 - Worked Example",
          "S5_Interpretation": "Scene 5 - Interpretation",
          "S6_Summary": "Scene 6 - Summary & Credits"}
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VIDS = os.path.join(HERE, "media", "videos", "gaussian_elimination", "1080p30")


def stamp(t, srt=False):
    m, s = divmod(t, 60)
    h, m = divmod(int(m), 60)
    if srt:
        return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
    return f"{m}:{s:04.1f}"


def mix_ai_voice():
    """Place each line's WAV at its cue start time -> audio/voiceover.wav."""
    import hashlib
    import numpy as np
    import soundfile as sf
    sr, clips, offset = 24000, [], 0.0
    for s in SCENES:
        d = json.load(open(os.path.join(HERE, "cues", s + ".json")))
        for c in d["cues"]:
            t = c["text"].strip()
            if t:
                k = hashlib.md5(t.encode()).hexdigest()[:10]
                clips.append((offset + c["start"], os.path.join(HERE, "audio", k + ".wav")))
        offset += d["duration"]
    track = np.zeros(int(offset * sr) + sr, dtype=np.float32)
    for start, path in clips:
        a, r = sf.read(path, dtype="float32")
        assert r == sr
        i = int(start * sr)
        track[i:i + len(a)] += a[:len(track) - i]
    out = os.path.join(HERE, "audio", "voiceover.wav")
    sf.write(out, track, sr)
    return out


def main():
    with open(os.path.join(HERE, "concat.txt"), "w") as f:
        for s in SCENES:
            f.write(f"file '{os.path.join(VIDS, s + '.mp4')}'\n")
    silent = os.path.join(ROOT, "_Video.mp4")
    tmp = silent.replace(".mp4", ".part.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", os.path.join(HERE, "concat.txt"), "-c", "copy",
                    "-movflags", "+faststart", tmp], check=True)
    voice = None
    if "--voice" in sys.argv:
        voice = sys.argv[sys.argv.index("--voice") + 1]
    elif "--silent" not in sys.argv:
        voice = mix_ai_voice()
    if voice:
        tmp2 = tmp.replace(".part", ".voice.part")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-i", voice,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac",
                        "-b:a", "192k", "-ar", "48000", "-shortest", tmp2], check=True)
        os.replace(tmp2, tmp)
    os.replace(tmp, silent)

    offset, n, srt, md = 0.0, 1, [], ["# Narration Script - Gaussian Elimination\n",
                                       "Read each line while the matching animation plays. "
                                       "Times are from the start of the video.\n"]
    for s in SCENES:
        d = json.load(open(os.path.join(HERE, "cues", s + ".json")))
        md.append(f"\n## {TITLES[s]}  ({stamp(offset)} - {stamp(offset + d['duration'])})\n")
        for c in d["cues"]:
            if not c["text"].strip():
                continue
            a, b = offset + c["start"], offset + c["end"]
            md.append(f"- **[{stamp(a)}]** {c['text']}")
            srt.append(f"{n}\n{stamp(a, True)} --> {stamp(b, True)}\n{c['text']}\n")
            n += 1
        offset += d["duration"]
    md.append(f"\n**Total length: {stamp(offset)}** "
              f"({sum(len(l.split()) for l in md)} words incl. headings)\n")
    open(os.path.join(ROOT, "Narration_Script.md"), "w").write("\n".join(md))
    open(os.path.join(ROOT, "narration.srt"), "w").write("\n".join(srt))
    print(f"wrote {silent}  ({offset:.1f} s)")


if __name__ == "__main__":
    main()
