# -*- coding: utf-8 -*-
"""Tests for GGS module."""

import numpy as np
import pytest

from sktime.annotation.ggs import GreedyGaussianSegmentation, get_GGS
from sktime.utils.validation._dependencies import _check_soft_dependencies


@pytest.fixture
def univariate_mean_shift():
    """Generate simple mean shift time series."""
    x = np.concatenate(tuple(np.ones(5) * i**2 for i in range(4)))
    return x[:, np.newaxis]


@pytest.mark.skipif(
    not _check_soft_dependencies("attrs", severity="none"),
    reason="skip test if required soft dependencies not available",
)
def test_GGS_find_change_points(univariate_mean_shift):
    """Test the GGS core estimator."""
    GGS = get_GGS()
    ggs = GGS(k_max=10, lamb=1.0)
    pred = ggs.find_change_points(univariate_mean_shift)
    assert isinstance(pred, list)
    assert len(pred) == 5


@pytest.mark.skipif(
    not _check_soft_dependencies("attrs", severity="none"),
    reason="skip test if required soft dependencies not available",
)
def test_GreedyGaussianSegmentation(univariate_mean_shift):
    """Test the GreedyGaussianSegmentation."""
    ggs = GreedyGaussianSegmentation(k_max=5, lamb=0.5)
    assert ggs.get_params() == {
        "k_max": 5,
        "lamb": 0.5,
        "verbose": False,
        "max_shuffles": 250,
        "random_state": None,
    }
