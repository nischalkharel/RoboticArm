import speech_recognition as sr

def listen_to_microphone():
    r = sr.Recognizer()

    # Specify the correct microphone by index
    mic = sr.Microphone(device_index=2)  # Use card 2, which is your USB microphone

    print("Start talking!")

    while True:
        with mic as source:
            print("Listening...")
            try:
                # Adjust for ambient noise for better accuracy
                r.adjust_for_ambient_noise(source)
                
                # Listen and recognize
                audio = r.listen(source)
                words = r.recognize_google(audio)
                print(f"You said: {words}")
                return words
            except sr.UnknownValueError:
                print("Sorry, could not understand the audio")
                sorry_message = "Sorry, could not understand the audio"
                return sorry_message
            except sr.RequestError:
                print("Could not request results; check your internet connection")
                internet_message = "Could not request results; check your internet connection"
                return internet_message
