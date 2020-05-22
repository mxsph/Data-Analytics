import json
import os
import shutil
import unittest

from visuanalytics.analytics.preprocessing.weather import transform
from visuanalytics.analytics.preprocessing.weather import speech as pre_speech
from visuanalytics.analytics.processing.weather import speech_single as pro_speech_single
from visuanalytics.analytics.util import date_time
from visuanalytics.analytics.util import resources


class ProcessTest(unittest.TestCase):
    with resources.open_resource("exampledata/example_weather.json") as file_handle:
        input = json.loads(file_handle.read())
        output = transform.preprocess_weather_data(input, True)
        cityname = "Kiel"
        date = date_time.date_to_weekday(transform.get_first_day_single(output, cityname))
        os.mkdir(resources.get_resource_path("temp/pre_1"))

    def test_if_get_all_audios_single_city_generates_audio(self):
        expected = pro_speech_single.get_all_audios_single_city("pre_1", self.output, self.date[0:5], self.cityname)
        assert os.path.exists(resources.get_resource_path(expected)) == 1

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(resources.get_resource_path("temp/pre_1"), ignore_errors=True)
