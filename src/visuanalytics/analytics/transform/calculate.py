import collections

import numpy as np

from visuanalytics.analytics.control.procedures.step_data import StepData
from visuanalytics.analytics.transform.util.key_utils import get_new_keys

CALCULATE_ACTIONS = {}


def register_calculate(func):
    CALCULATE_ACTIONS[func.__name__.replace("calculate_", "")] = func
    return func


@register_calculate
def calculate_mean(values: dict, data: StepData):
    """Berechnet den Mittelwert von Werten, die in einem Array stehen.

    :param values: Werte aus der JSON-Datei
    :param data: Daten aus der API
    :return:
    """
    for idx, key in data.loop_key(values["keys"], values):
        value = data.get_data(key, values)
        new_key = get_new_keys(values, idx)
        mean_value = float(np.mean(value))
        if values.get("decimal", None):
            new_value = round(mean_value, data.format(values["decimal"], values))
        else:
            new_value = round(mean_value)
        data.insert_data(new_key, new_value, values)


@register_calculate
def calculate_max(values: dict, data: StepData):
    """Sucht den Maximalwert von Werten, die in einem Array stehen.

    :param values: Werte aus der JSON-Datei
    :param data: Daten aus der API
    """
    for idx, key in data.loop_key(values["keys"], values):
        value = data.get_data(key, values)
        new_key = get_new_keys(values, idx)
        new_value = max(value)
        data.insert_data(new_key, new_value, values)

        if values.get("save_idx_to", None):
            data.insert_data(values["save_idx_to"][idx], value.index(new_value), values)


@register_calculate
def calculate_min(values: dict, data: StepData):
    """Sucht den Minimalwert von Werten, die in einem Array stehen.

    :param values: Werte aus der JSON-Datei
    :param data: Daten aus der API
    """
    for idx, key in data.loop_key(values["keys"], values):
        value = data.get_data(key, values)
        new_key = get_new_keys(values, idx)
        new_value = min(value)
        data.insert_data(new_key, new_value, values)

        if values.get("save_idx_to", None):
            data.insert_data(values["save_idx_to"][idx], value.index(new_value), values)


@register_calculate
def calculate_round(values: dict, data: StepData):
    """Rundet gegebene Werte auf eine gewünschte Nachkommastelle ab.

    :param values: Werte aus der JSON-Datei
    :param data: Daten aus der API
    """
    for idx, key in data.loop_key(values["keys"], values):
        value = data.get_data(key, values)
        new_key = get_new_keys(values, idx)

        if values.get("decimal", None):
            new_value = round(value, data.format(values["decimal"], values))
        else:
            new_value = round(value)
        data.insert_data(new_key, new_value, values)


@register_calculate
def calculate_mode(values: dict, data: StepData):
    """Bestimmt den am häufigsten in einem Array vorkommenden Value.

    :param values: Werte aus der JSON-Datei
    :param data: Daten aus der API
    """
    for idx, key in data.loop_key(values["keys"], values):
        value = data.get_data(key, values)
        new_key = get_new_keys(values, idx)
        new_value = collections.Counter(value).most_common()[0][0]
        data.insert_data(new_key, new_value, values)


@register_calculate
def calculate_ms_to_kmh(values: dict, data: StepData):
    """Wandelt den angegebenen Wert von m/s in km/h um und rundet auf die 2. Nachkommastelle.

    :param values: Werte aus der JSON-Datei
    :param data: Daten aus der API
    """
    for idx, key in data.loop_key(values["keys"], values):
        value = data.get_data(key, values)
        new_key = get_new_keys(values, idx)
        kmh = (value * 3.6)
        if values.get("decimal", None):
            new_value = round(kmh, data.format(values["decimal"], values))
        else:
            new_value = round(kmh)
        data.insert_data(new_key, new_value, values)


@register_calculate
def calculate_subtract(values: dict, data: StepData):
    for idx, key in data.loop_key(values["keys"], values):
        value = int(data.get_data(key, values))
        subtract = int(data.get_data(values["subtract"][idx], values))
        new_key = get_new_keys(values, idx, key)
        new_value = value - subtract
        data.insert_data(new_key, new_value, values)


@register_calculate
def calculate_add(values: dict, data: StepData):
    for idx, key in data.loop_key(values["keys"], values):
        value = int(data.get_data(key, values))
        add = int(data.get_data(values["add"][idx], values))
        new_key = get_new_keys(values, idx, key)
        new_value = value + add
        data.insert_data(new_key, new_value, values)
