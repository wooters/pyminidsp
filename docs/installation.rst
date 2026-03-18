Installation
============

Installing from PyPI (pre-built wheels)
---------------------------------------

Pre-built wheels are available for **Linux** x86-64 and **macOS** ARM64
(Apple Silicon), with Python 3.9–3.13. Wheels include the compiled C
extension, so no C compiler is needed. However, the FFTW3 runtime library
must be installed on your system.

Install FFTW3:

**Ubuntu / Debian**

.. code-block:: bash

   sudo apt install libfftw3-3

**macOS (Homebrew)**

.. code-block:: bash

   brew install fftw

**Fedora / RHEL**

.. code-block:: bash

   sudo dnf install fftw-libs

Then install pyminidsp:

.. code-block:: bash

   pip install pyminidsp


Building from source
--------------------

If you need to build from source (e.g. unsupported platform or development),
you will need the following **in addition to** the FFTW3 runtime library above:

- `FFTW3 <http://www.fftw.org/>`_ **development headers**
  (Ubuntu/Debian: ``libfftw3-dev``, Fedora/RHEL: ``fftw-devel``,
  macOS: included with ``brew install fftw``)
- A C compiler (gcc or clang)
- The `miniDSP <https://github.com/wooters/miniDSP>`_ C library source

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
