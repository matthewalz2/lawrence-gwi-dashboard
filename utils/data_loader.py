import pandas as pd


def read_csv_fallback(path, encodings=None, **kwargs):
    """Attempt to read a CSV using several encodings until one succeeds.

    Args:
        path: Path to CSV file.
        encodings: Iterable of encoding names to try.
        **kwargs: Passed to pandas.read_csv.

    Returns:
        pandas.DataFrame

    Raises:
        Exception: The last exception raised if all encodings fail.
    """
    if encodings is None:
        encodings = ["utf-8", "utf-8-sig", "cp1252", "latin1", "utf-16"]

    last_exc = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc, **kwargs)
        except Exception as e:
            last_exc = e
    raise last_exc
