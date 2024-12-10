import subprocess

def speak_text(text):
    subprocess.run(["espeak", text])
