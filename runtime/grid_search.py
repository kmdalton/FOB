from pathlib import Path
import json
from typing import Iterator, Any
from math import log10, floor


def load_json(json_data: Path | str) -> dict:
    if isinstance(json_data, Path):
        with open(json_data, "r", encoding="utf8") as f:
            parsed = json.load(f)
    elif isinstance(json_data, str):
        parsed = json.loads(json_data)
    else:
        return json_data
    return parsed


def is_search_space(json_data: Path | str | dict) -> bool:
    """Checks if the json has a list as value"""
    if isinstance(json_data, (Path, str)):
        json_data = load_json(json_data)
    for v in json_data.values():
        if isinstance(v, list):
            return True
    return False


def generate_hyperparameter_from_search_space(json_data: Path | str | dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Generates hyperparameter using grid search from search space

    Each combination is generated!"""
    if isinstance(json_data, (Path, str)):
        json_data = load_json(json_data)
    # find first list and iterate over it
    for k, v in json_data.items():
        if isinstance(v, list):
            for hp_value in v:
                subset = json_data.copy()
                subset.pop(k)
                subsets = generate_hyperparameter_from_search_space(subset)
                for s in subsets:
                    yield {k: hp_value} | s
            break
    else:
        # no list found
        yield json_data


def write_hyperparameter(search_space: Path, output_dir: Path) -> int:
    """Write hyperparameter from search space to folder returning the number oif files generated"""
    hps = list(generate_hyperparameter_from_search_space(search_space))
    padding = floor(log10(len(hps) - 1)) + 1
    for i, hp in enumerate(hps):
        with open(output_dir / (str(i).zfill(padding) + ".json"), "w", encoding="utf8") as f:
            json.dump(hp, f, indent=4)
    return len(hps)


def unique_append(xs, x):
    if x not in xs:
        xs.append(x)


def gridsearch(d: dict[str, Any]) -> list[dict[str, Any]]:
    ret = []
    if isinstance(d, dict):
        for k, v in d.items():
            options = gridsearch(v)
            rest = d.copy()
            rest.pop(k)
            other_options = gridsearch(rest)
            for o1 in options:
                if other_options:
                    for o2 in other_options:
                        unique_append(ret, o2 | {k: o1})
                else:
                    ret.append(rest | {k: o1})
    elif isinstance(d, list):
        for v in d:
            options = gridsearch(v)
            for option in options:
                unique_append(ret, option)
    else:
        ret.append(d)
    return ret
