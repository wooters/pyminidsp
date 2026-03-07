"""Tests for internal helpers and input type coercion."""

import numpy as np
import pytest

import pyminidsp as md
from pyminidsp._helpers import _as_double_ptr, _new_double_array, shutdown


class TestNewDoubleArray:
    def test_shape_and_dtype(self):
        arr, ptr = _new_double_array(10)
        assert arr.shape == (10,)
        assert arr.dtype == np.float64

    def test_initialized_to_zero(self):
        arr, _ = _new_double_array(50)
        np.testing.assert_array_equal(arr, 0.0)

    def test_single_element(self):
        arr, _ = _new_double_array(1)
        assert arr.shape == (1,)


class TestAsDoublePtr:
    def test_contiguous_float64_no_copy(self):
        arr = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        ptr, result = _as_double_ptr(arr)
        assert result.dtype == np.float64
        assert result.flags["C_CONTIGUOUS"]

    def test_float32_coercion(self):
        arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        ptr, result = _as_double_ptr(arr)
        assert result.dtype == np.float64

    def test_int32_coercion(self):
        arr = np.array([1, 2, 3], dtype=np.int32)
        ptr, result = _as_double_ptr(arr)
        assert result.dtype == np.float64

    def test_int64_coercion(self):
        arr = np.array([1, 2, 3], dtype=np.int64)
        ptr, result = _as_double_ptr(arr)
        assert result.dtype == np.float64

    def test_non_contiguous(self):
        arr = np.arange(10, dtype=np.float64)[::2]
        assert not arr.flags["C_CONTIGUOUS"]
        ptr, result = _as_double_ptr(arr)
        assert result.flags["C_CONTIGUOUS"]
        assert result.dtype == np.float64


class TestShutdown:
    def test_callable(self):
        shutdown()


class TestInputCoercion:
    """Verify representative functions accept non-float64 inputs."""

    def test_rms_int32(self):
        arr = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        result = md.rms(arr)
        assert isinstance(result, float)
        assert result > 0

    def test_rms_int64(self):
        arr = np.array([1, 2, 3, 4, 5], dtype=np.int64)
        result = md.rms(arr)
        assert isinstance(result, float)

    def test_rms_float32(self):
        arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        result = md.rms(arr)
        assert isinstance(result, float)

    def test_magnitude_spectrum_float32(self):
        arr = np.ones(64, dtype=np.float32)
        mag = md.magnitude_spectrum(arr)
        assert mag.dtype == np.float64

    def test_convolution_time_int32(self):
        sig = np.array([1, 0, 0, 0, 0], dtype=np.int32)
        kernel = np.array([1, 2, 3], dtype=np.int32)
        out = md.convolution_time(sig, kernel)
        assert out.dtype == np.float64
        np.testing.assert_allclose(out[:3], [1.0, 2.0, 3.0])

    def test_non_contiguous_input(self):
        arr = np.arange(20, dtype=np.float64)[::2]  # non-contiguous
        result = md.rms(arr)
        assert isinstance(result, float)
        assert result > 0
