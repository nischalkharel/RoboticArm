from audio_in import listen_to_microphone
from audio_out import speak_text

def speech():
    recognized_text = listen_to_microphone()
    if recognized_text == " activate now":
        return recognized_text

if __name__ == "__main__":
    while True:
        recognized_text = listen_to_microphone()
        if recognized_text == "activate now":
            speak_text("Please, wait,    The arm, is, activating!")
