import pandas as pd
import numpy as np
from datetime import datetime


def df_to_dicts(df: pd.DataFrame):
    """
    df to list dict
    """
    return [{k: None if pd.isnull(v) else v for k, v in dict(df.iloc[i]).items()} for i in range(len(df))]


def series_to_d(s: pd.Series):
    return {k: None if pd.isnull(v) else v for k, v in dict(s).items()}


unix_epoch = np.datetime64(0, 's')
one_second = np.timedelta64(1, 's')

def np_dt_to_py_dt(t: np.datetime64) -> datetime:
    datetime.utcfromtimestamp(t - unix_epoch / one_second)


json_converters = {
    np.bool_: bool,
    np.bool8: bool,
    np.int8: int,
    np.int32: int,
    np.int64: int,
    np.uint8: int,
    np.uint32: int,
    np.uint64: int,
    np.uint: int,
    np.int_: int,
    np.float_: float,
    np.float16: float,
    np.float32: float,
    np.float64: float,
    np.datetime64: np_dt_to_py_dt,
    np.ndarray: lambda x: x.tolist(),
    pd.Timestamp: lambda x: x.to_pydatetime(),
    pd.DataFrame: df_to_dicts,
}
