## 1. Restructure docs/installation.rst

- [x] 1.1 Remove the top-level "Prerequisites" section that lists C compiler and FFTW3 dev headers
- [x] 1.2 Rewrite the opening section for wheel installs — lead with FFTW3 runtime library install instructions (e.g., `apt install libfftw3-3`, `brew install fftw`), then `pip install pyminidsp`, list supported platforms/Python versions, and note that no C compiler is needed
- [x] 1.3 Create a "Building from Source" section that includes the C compiler, FFTW3 dev headers, and MINIDSP_SRC prerequisites, plus the source install commands
- [x] 1.4 Keep the "Development install" section intact, nested under or after "Building from Source"

## 2. Update README.md

- [x] 2.1 Update the note under the "Installation" heading to clarify that pre-built wheels require FFTW3 at runtime but not a C compiler

## 3. Verify

- [x] 3.1 Build Sphinx docs (`cd docs && make html`) and confirm no new warnings or broken links
- [x] 3.2 Visually review the rendered installation page for clarity and correct section ordering
