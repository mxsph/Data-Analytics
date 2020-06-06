import json

from gtts import gTTS

from visuanalytics.analytics.processing.audio.parts import part
from visuanalytics.analytics.util import resources


def generate_audio(name, value, config):
    text = part.audio_parts(value["parts"])
    tts = gTTS(text, config["lang"])
    file_path = resources.new_temp_resource_path(name, config["format"])
    tts.save(file_path)
    return file_path


with open("/exampledata/step-example_weather_single_test.json") as fp:
    d = json.loads(fp)

x = generate_audio(d["name"], d["audio"]["audios"]["a1"], d["audio"]["config"])
print(x)
