## 1. Restructure Installation Section

- [x] 1.1 Replace the current Prerequisites + Installation sections with a new Installation section that leads with `pip install pyminidsp`
- [x] 1.2 Add platform support note listing wheel availability (Linux x86-64, macOS ARM64, Python 3.9–3.13)
- [x] 1.3 Add a "Building from Source" subsection with prerequisites (FFTW3, C compiler) and the existing `uv sync` instructions

## 2. Complete API Overview

- [x] 2.1 Add Window Functions table (`hann_window`, `hamming_window`, `blackman_window`, `rect_window`)
- [x] 2.2 Add Signal Measurement table (`dot`, `entropy`, `mix`)
- [x] 2.3 Add Signal Scaling table (`scale`, `scale_vec`, `fit_within_range`, `adjust_dblevel`)
- [x] 2.4 Add missing utility functions to existing tables (`convolution_num_samples`, `stft_num_frames`, `dtmf_signal_length`, `steg_capacity`, `get_multiple_delays`)

## 3. Verify

- [x] 3.1 Confirm all publicly exported symbols from `__init__.py` appear in the API Overview
- [x] 3.2 Review final README renders correctly as markdown
