## ADDED Requirements

### Requirement: Generate llms.txt index file
The script SHALL produce an `llms.txt` file in the specified output directory containing:
- The project name (`pyminidsp`)
- A one-line project description
- A URL pointing to `llms-full.txt` on the deployed docs site (`https://wooters.github.io/pyminidsp/llms-full.txt`)
- A URL pointing to the project's GitHub repository

#### Scenario: llms.txt contains project summary and pointer
- **WHEN** the generation script is run
- **THEN** `llms.txt` is written to the output directory with the project name, description, and a link to `llms-full.txt` on the deployed docs site

#### Scenario: llms.txt is concise
- **WHEN** the generation script is run
- **THEN** `llms.txt` SHALL be fewer than 20 lines

### Requirement: Generate llms-full.txt API reference
The script SHALL produce an `llms-full.txt` file in the specified output directory containing a complete API reference section. For each public function exported by pyminidsp, the reference SHALL include:
- Function signature (name and parameters)
- Docstring content (description, parameter docs, return value docs)
- Functions grouped by category (matching the module organization: analysis, effects, filters, spectral, generators, dtmf, gcc, resampling, steganography, helpers/constants)

#### Scenario: All public API functions are documented
- **WHEN** the generation script is run
- **THEN** every symbol listed in `pyminidsp.__all__` SHALL appear in the API reference section of `llms-full.txt`

#### Scenario: Function entries include signature and docstring
- **WHEN** a public function is documented in `llms-full.txt`
- **THEN** its entry SHALL include the function signature and its full docstring text

#### Scenario: Functions are grouped by category
- **WHEN** the API reference is generated
- **THEN** functions SHALL be organized under category headings that match their source module

### Requirement: Generate llms-full.txt tutorials section
The script SHALL include a tutorials section in `llms-full.txt` that contains content extracted from the RST guide files in `docs/guides/`.

#### Scenario: All guides are included
- **WHEN** the generation script is run
- **THEN** every `.rst` file in `docs/guides/` SHALL have its content included in the tutorials section

#### Scenario: RST markup is stripped
- **WHEN** guide content is included in `llms-full.txt`
- **THEN** RST-specific directives (e.g., `.. code-block::`, `.. plot::`, `.. note::`, role markup like `:func:`, `:math:`) SHALL be converted to plain text or markdown equivalents

#### Scenario: Code examples are preserved
- **WHEN** a guide contains `.. code-block::` or literal block content
- **THEN** the code content SHALL be preserved as fenced code blocks in the output

### Requirement: Script runs standalone
The generation script SHALL be executable as `python scripts/gen_llms_txt.py` from the project root, requiring only that pyminidsp is installed in the current environment. It SHALL accept an optional output directory argument (defaulting to `docs/_build/html/`).

#### Scenario: Standalone execution
- **WHEN** `python scripts/gen_llms_txt.py` is run in an environment where pyminidsp is installed
- **THEN** both `llms.txt` and `llms-full.txt` are written to the output directory

#### Scenario: Custom output directory
- **WHEN** `python scripts/gen_llms_txt.py --output-dir /path/to/dir` is run
- **THEN** both files are written to the specified directory

#### Scenario: Missing pyminidsp produces clear error
- **WHEN** the script is run in an environment where pyminidsp is not installed
- **THEN** the script SHALL exit with a clear error message indicating pyminidsp must be installed

### Requirement: Output structure matches miniDSP convention
The generated files SHALL follow the same structural conventions as the miniDSP C library's llms.txt files:
- Section headers with `#` markdown headings
- Entries separated by `---` dividers
- Code examples in fenced code blocks

#### Scenario: Consistent formatting with miniDSP
- **WHEN** the output files are generated
- **THEN** they SHALL use markdown headings, `---` dividers between entries, and fenced code blocks for examples
