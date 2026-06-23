import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile

# Load model once when program starts
model = whisper.load_model("base")


def listen():

    fs = 44100
    duration = 5  # seconds

    print("\nListening...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1
    )

    sd.wait()

    print("Processing speech...")

    with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
    ) as temp_audio:

        write(
            temp_audio.name,
            fs,
            recording
        )

        result = model.transcribe(temp_audio.name)

    text = result["text"].strip()

    print(f"You said: {text}")

    return text