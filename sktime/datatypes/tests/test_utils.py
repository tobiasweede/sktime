# -*- coding: utf-8 -*-
"""Testing utilities in the datatype module."""

__author__ = ["fkiraly"]

import numpy as np
import pandas as pd
import pytest

from sktime.datatypes._check import check_is_mtype
from sktime.datatypes._examples import get_examples
from sktime.datatypes._utilities import get_cutoff, get_slice, get_window

SCITYPE_MTYPE_PAIRS = [
    ("Series", "pd.Series"),
    ("Series", "pd.DataFrame"),
    ("Series", "np.ndarray"),
    ("Panel", "pd-multiindex"),
    ("Panel", "numpy3D"),
    ("Panel", "nested_univ"),
    ("Panel", "df-list"),
    ("Hierarchical", "pd_multiindex_hier"),
]


@pytest.mark.parametrize("return_index", [True, False])
@pytest.mark.parametrize("scitype,mtype", SCITYPE_MTYPE_PAIRS)
def test_get_cutoff(scitype, mtype, return_index):
    """Tests that conversions for scitype agree with from/to example fixtures.

    Parameters
    ----------
    scitype : str - scitype of input
    mtype : str - mtype of input
    return_index : bool - whether index (True) or index element is returned (False)

    Raises
    ------
    AssertionError if get_cutoff does not return a length 1 pandas.index
        for any fixture example of given scitype, mtype
    """
    # retrieve example fixture
    fixtures = get_examples(mtype=mtype, as_scitype=scitype, return_lossy=False)

    for fixture in fixtures.values():
        if fixture is None:
            continue

        cutoff = get_cutoff(fixture, return_index=return_index)

        if return_index:
            expected_types = pd.Index
        else:
            expected_types = (int, float, np.int64, pd.Timestamp)

        msg = (
            f"incorrect return type of get_cutoff"
            f"expected {expected_types}, found {type(cutoff)}"
        )

        assert isinstance(cutoff, expected_types), msg

        if return_index:
            assert len(cutoff) == 1


@pytest.mark.parametrize("window_length, lag", [(2, 0), (None, 0), (4, 1)])
@pytest.mark.parametrize("scitype,mtype", SCITYPE_MTYPE_PAIRS)
def test_get_window_output_type(scitype, mtype, window_length, lag):
    """Tests that get_window runs for all mtypes, and returns output of same mtype.

    Parameters
    ----------
    scitype : str - scitype of input
    mtype : str - mtype of input
    window_length : int, passed to get_window
    lag : int, passed to get_window

    Raises
    ------
    Exception if get_window raises one
    """
    # retrieve example fixture
    fixture = get_examples(mtype=mtype, as_scitype=scitype, return_lossy=False)[0]
    X = get_window(fixture, window_length=window_length, lag=lag)
    valid, err, _ = check_is_mtype(X, mtype=mtype, return_metadata=True)

    msg = (
        f"get_window should return an output of mtype {mtype} for that type of input, "
        f"but it returns an output not conformant with that mtype."
        f"Error from mtype check: {err}"
    )

    assert valid, msg


def test_get_window_expected_result():
    """Tests that get_window produces return of the right length.

    Raises
    ------
    Exception if get_window raises one
    AssertionError if get_window output shape is not as expected
    """
    X_df = get_examples(mtype="pd.DataFrame")[0]
    assert len(get_window(X_df, 2, 1)) == 2
    assert len(get_window(X_df, 3, 1)) == 3
    assert len(get_window(X_df, 1, 2)) == 1
    assert len(get_window(X_df, 3, 4)) == 0
    assert len(get_window(X_df, 3, None)) == 3
    assert len(get_window(X_df, None, 2)) == 2
    assert len(get_window(X_df, None, None)) == 4

    X_mi = get_examples(mtype="pd-multiindex")[0]
    assert len(get_window(X_mi, 3, 1)) == 6
    assert len(get_window(X_mi, 2, 0)) == 6
    assert len(get_window(X_mi, 2, 4)) == 0
    assert len(get_window(X_mi, 1, 2)) == 3
    assert len(get_window(X_mi, 2, None)) == 6
    assert len(get_window(X_mi, None, 2)) == 3
    assert len(get_window(X_mi, None, None)) == 9

    X_hi = get_examples(mtype="pd_multiindex_hier")[0]
    assert len(get_window(X_hi, 3, 1)) == 12
    assert len(get_window(X_hi, 2, 0)) == 12
    assert len(get_window(X_hi, 2, 4)) == 0
    assert len(get_window(X_hi, 1, 2)) == 6
    assert len(get_window(X_hi, 2, None)) == 12
    assert len(get_window(X_hi, None, 2)) == 6
    assert len(get_window(X_hi, None, None)) == 18

    X_np3d = get_examples(mtype="numpy3D")[0]
    assert get_window(X_np3d, 3, 1).shape == (2, 2, 3)
    assert get_window(X_np3d, 2, 0).shape == (2, 2, 3)
    assert get_window(X_np3d, 2, 4).shape == (0, 2, 3)
    assert get_window(X_np3d, 1, 2).shape == (1, 2, 3)
    assert get_window(X_np3d, 2, None).shape == (2, 2, 3)
    assert get_window(X_np3d, None, 2).shape == (1, 2, 3)
    assert get_window(X_np3d, None, None).shape == (3, 2, 3)


@pytest.mark.parametrize("scitype,mtype", SCITYPE_MTYPE_PAIRS)
def test_get_slice_output_type(scitype, mtype):
    """Tests that get_slice runs for all mtypes, and returns output of same mtype.

    Parameters
    ----------
    scitype : str - scitype of input
    mtype : str - mtype of input

    Raises
    ------
    Exception if get_slice raises one
    """
    # retrieve example fixture
    fixture = get_examples(mtype=mtype, as_scitype=scitype, return_lossy=False)[0]
    X = get_slice(fixture)
    valid, err, _ = check_is_mtype(X, mtype=mtype, return_metadata=True)

    msg = (
        f"get_slice should return an output of mtype {mtype} for that type of input, "
        f"but it returns an output not conformant with that mtype."
        f"Error from mtype check: {err}"
    )

    assert valid, msg


def test_get_slice_expected_result():
    """Tests that get_slice produces return of the right length.

    Raises
    ------
    Exception if get_slice raises one
    """
    X_df = get_examples(mtype="pd.DataFrame")[0]
    assert len(get_slice(X_df, start=1, end=3)) == 2

    X_s = get_examples(mtype="pd.Series")[0]
    assert len(get_slice(X_s, start=1, end=3)) == 2

    X_np = get_examples(mtype="numpy3D")[0]
    assert get_slice(X_np, start=1, end=3).shape == (2, 2, 3)
