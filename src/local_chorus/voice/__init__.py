"""Voice IO — STT in, TTS out, wake-word detection.

Wiring will be:
- wake word: openWakeWord (added in roadmap chapter 6, q26)
- STT: whisper.cpp via subprocess
- TTS: piper-tts via subprocess (added in roadmap chapter 6)

For now the module is just a placeholder — implementations land as the
roadmap reaches them.
"""
