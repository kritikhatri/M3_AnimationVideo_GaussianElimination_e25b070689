# M3 Animation Video: Gaussian Elimination

**Student:** Kritika Khatri · **Student ID:** e25b070689 · **Batch:** Ramanujan
**Course:** Linear Algebra and Calculus (M3), Internal Assessment, Project Option 1

**Learning objective:** By the end of this video, the viewer will be able to reduce a 3 × 3 system to row echelon form using elementary row operations, solve it by back-substitution, and explain why row operations preserve the solution set.

## Repository contents
| File | What it is |
|---|---|
| `_Video.mp4` | Final video, 1920×1080, 16:9, 30 fps, MP4 (H.264 + AAC voice-over) |
| `_Code/gaussian_elimination.py` | Manim source, with one class per storyboard scene (`S1_Hook` … `S6_Summary`) |
| `_Code/make_voiceover.py` | Generates the voice-over lines with Kokoro TTS (offline) |
| `_Code/audio/` | Voice-over WAV per narration line and `durations.json` (timings) |
| `_Code/build_video.py` | Joins the six scenes into `_Video.mp4` and mixes in the voice-over |
| `_Code/verify_math.py` | Exact-fraction check of every number shown in the video |
| `_Code/make_storyboard.py` | Builds `Storyboard.pdf` from the rendered scenes |
| `Storyboard.pdf` | 6-scene storyboard: purpose, visuals, narration and maths plan |
| `Narration_Script.md` / `narration.srt` | Voice-over script with timings |
| `AI_Disclosure.md` | Every AI tool used and what it did |

## Worked example
```
 x +  y +  z =  6           R2 → R2 − 2R1   [0 −1 −3 | −11]
2x +  y −  z =  1    →      R3 → R3 −  R1   [0 −2  1 |  −1]
 x −  y + 2z =  5           R3 → R3 − 2R2   [0  0  7 |  21]   ⇒  z = 3, y = 2, x = 1
```

## How to reproduce
```bash
pip install manim            # also needs LaTeX (MiKTeX / TeX Live) and ffmpeg
cd _Code
python make_voiceover.py --model kokoro-v1.0.onnx --voices voices-v1.0.bin   # optional: regenerate voice
manim -r 1920,1080 --frame_rate 30 gaussian_elimination.py S1_Hook S2_Concept S3_Intuition S4_Example S5_Interpretation S6_Summary
python verify_math.py
python build_video.py          # or: --voice my_recording.m4a
python make_storyboard.py
```

## Credits
- G. Strang, *Introduction to Linear Algebra*, 5th ed., Chapter 2
- D. C. Lay, *Linear Algebra and Its Applications*, Chapter 1
- M3 lecture notes, Newton School of Technology
- Animation: [Manim Community Edition](https://www.manim.community/) · Editing: ffmpeg
- Voice-over: AI text-to-speech, [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) (voice `af_heart`)
- Music: none

## AI disclosure
The script, storyboard and Manim code were drafted with help from Claude (Anthropic). The voice-over is AI text-to-speech (Kokoro). I checked all the mathematics by hand (see `verify_math.py`).

Full details: [AI_Disclosure.md](AI_Disclosure.md)
