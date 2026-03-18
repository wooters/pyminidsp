"""Tests for the miniDSP error handling infrastructure."""

import threading

import pytest

import pyminidsp as md
from pyminidsp._helpers import MiniDSPError, _check_error, _error_state


class TestMiniDSPErrorClass:
    def test_importable_from_package(self):
        from pyminidsp import MiniDSPError as Err
        assert Err is MiniDSPError

    def test_is_runtime_error_subclass(self):
        assert issubclass(MiniDSPError, RuntimeError)

    def test_carries_attributes(self):
        err = MiniDSPError(2, "MD_foo", "size must be > 0")
        assert err.code == 2
        assert err.func_name == "MD_foo"
        assert err.message == "size must be > 0"
        assert "MD_foo" in str(err)
        assert "size must be > 0" in str(err)


class TestErrorCodeConstants:
    def test_values(self):
        assert md.ERR_NULL_POINTER == 1
        assert md.ERR_INVALID_SIZE == 2
        assert md.ERR_INVALID_RANGE == 3
        assert md.ERR_ALLOC_FAILED == 4

    def test_importable(self):
        from pyminidsp import (
            ERR_NULL_POINTER,
            ERR_INVALID_SIZE,
            ERR_INVALID_RANGE,
            ERR_ALLOC_FAILED,
        )
        assert ERR_NULL_POINTER == 1
        assert ERR_INVALID_SIZE == 2
        assert ERR_INVALID_RANGE == 3
        assert ERR_ALLOC_FAILED == 4


class TestCheckErrorClears:
    def test_no_error_does_nothing(self):
        _error_state.error = None
        _check_error()  # should not raise

    def test_clears_after_raise(self):
        _error_state.error = (2, "MD_test", "bad size")
        with pytest.raises(MiniDSPError):
            _check_error()
        # State should be cleared
        _check_error()  # should not raise

    def test_successful_call_after_error(self):
        """After catching an error, subsequent valid calls succeed."""
        _error_state.error = (1, "MD_test", "null pointer")
        with pytest.raises(MiniDSPError):
            _check_error()
        # A normal call should work fine
        result = md.sine_wave(64)
        assert len(result) == 64


class TestThreadSafety:
    def test_concurrent_threads_independent(self):
        """Errors in one thread don't leak to another."""
        results = {}

        def thread_with_error(tid):
            _error_state.error = (3, "MD_thread_test", f"error in {tid}")
            try:
                _check_error()
            except MiniDSPError as e:
                results[tid] = e.code

        def thread_no_error(tid):
            # Small sleep to let the error thread run first
            import time
            time.sleep(0.01)
            # This thread should have no error
            try:
                _check_error()
                results[tid] = "ok"
            except MiniDSPError:
                results[tid] = "unexpected_error"

        t1 = threading.Thread(target=thread_with_error, args=("err",))
        t2 = threading.Thread(target=thread_no_error, args=("clean",))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert results["err"] == 3
        assert results["clean"] == "ok"
