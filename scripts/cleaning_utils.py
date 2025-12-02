import pandas as pd
import numpy as np


def extract_name_from_dict(col, key="name"):
    """Extracts the 'name' field from a dictionary into 'name1|name2|...'"""
    if isinstance(col, list):
        values = [item.get(key, "") for item in col]
        return "|".join(values)
    return np.nan