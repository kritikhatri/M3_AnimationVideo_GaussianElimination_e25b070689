# AI Disclosure

**Project:** M3 Animation Video: Gaussian Elimination
**Student:** Kritika Khatri · **Student ID:** e25b070689 · **Batch:** Ramanujan

The M3 brief asks every student to disclose any AI tools used for scripting, visuals, voice or coding. This file lists every AI tool used in this project and what it did.

## AI tools used

| Tool | Used for | Part of the project |
|---|---|---|
| **Claude** (Anthropic, Claude Opus 5.5) | Script and coding assistant | Planned the 6 scenes, wrote the narration script, wrote the Manim animation code (`_Code/gaussian_elimination.py`) and the helper scripts (`build_video.py`, `make_storyboard.py`, `make_voiceover.py`, `verify_math.py`), and generated the storyboard PDF and README |
| **Kokoro TTS** (open-source, [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx), voice `af_heart`) | Voice | Read the narration script aloud to produce the voice-over in `_Video.mp4` |

## What was not AI-generated
- **The topic:** Gaussian elimination was chosen by the student from the approved M3 topic bank.
- **The animation:** the animations are produced by running the Manim code (Manim Community Edition). No AI image or video generator was used, and no existing video was screen-recorded.
- **Music:** none.

## How the mathematics was checked
- Every row operation, the back-substitution and the final answer (x, y, z) = (1, 2, 3) are checked with exact fractions in `_Code/verify_math.py`.
- The student checked the calculations by hand:
  - R2 − 2R1 = [0, −1, −3 | −11]
  - R3 − R1 = [0, −2, 1 | −1]
  - R3 − 2R2 = [0, 0, 7 | 21]
  - z = 3, y = 2, x = 1
  - all three original equations are satisfied.

## Student's role
- Chose the topic and the approach.
- Reviewed the script, storyboard and final video.
- Checked the mathematics independently.
- Uploaded and submitted the repository.
- Prepared to explain the derivations, visual choices and Manim code in the viva without relying on the video.
