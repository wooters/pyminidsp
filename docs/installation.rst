Installation
============

Prerequisites
-------------

- Python >= 3.9
- `FFTW3 <http://www.fftw.org/>`_ development headers
- A C compiler (gcc or clang)

Install FFTW3 for your platform:

.. tab-set-directive is not used here for simplicity

**Ubuntu / Debian**

.. code-block:: bash

   sudo apt install libfftw3-dev

**macOS (Homebrew)**

.. code-block:: bash

   brew install fftw

**Fedora / RHEL**

.. code-block:: bash

   sudo dnf install fftw-devel


Installing from PyPI (pre-built wheels)
---------------------------------------

.. code-block:: bash

   pip install pyminidsp

Pre-built wheels include the compiled C extension and bundled FFTW3 library,
so no C compiler or FFTW3 headers are needed.


Installing from source
----------------------

.. code-block:: bash

   # Clone the miniDSP C library
   git clone https://github.com/wooters/miniDSP.git

   # Install pyminidsp (set MINIDSP_SRC to point to the C library)
   MINIDSP_SRC=./miniDSP pip install .


Development install
-------------------

.. code-block:: bash

   git clone https://github.com/wooters/pyminidsp.git
   cd pyminidsp
   git clone https://github.com/wooters/miniDSP.git

   pip install cffi numpy
   MINIDSP_SRC=./miniDSP python pyminidsp/_build_minidsp.py
   pip install -e ".[dev,docs]"

   # Run the test suite
   python -m pytest tests/ -v

   # Build the documentation
   cd docs && make html
