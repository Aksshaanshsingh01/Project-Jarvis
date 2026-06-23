import pyttsx3


def speak(text):
    try:
        engine = pyttsx3.init()

        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print(f"Speech Error: {e}")