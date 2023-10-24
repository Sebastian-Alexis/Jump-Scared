from pydub import AudioSegment
from pydub.playback import play


def play_loud_sound(file_path):
    # Load the audio file
    sound = AudioSegment.from_file(file_path, format="mp3")

    # Boost the volume (you can adjust the value based on how loud you want it to be)
    loud_sound = sound + 20  # Increase volume by 20dB

    # Play the loud sound
    play(loud_sound)


if __name__ == "__main__":
    play_loud_sound("jumpscare_media/jumpscare.mp3")
