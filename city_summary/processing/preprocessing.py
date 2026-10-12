RAINY_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}


def is_warm_clothes(temp: float) -> bool:
    return temp < 0


def is_expensive(rate: float) -> bool:
    return rate > 100


def take_umbrella(desc_code) -> bool:
    return desc_code in RAINY_CODES


def apply_preprocessing(summary: dict, desc_code=None) -> dict:
    summary["weather"]["warm_clothes"] = is_warm_clothes(summary["weather"]["temp_c"])
    summary["rates"]["expensive"] = is_expensive(summary["rates"]["rate_to_rub"])
    if not summary["weather"]["description"]:
        summary["weather"]["description"] = "unknown"
    if desc_code is not None:
        summary["weather"]["umbrella"] = take_umbrella(desc_code)
    return summary
