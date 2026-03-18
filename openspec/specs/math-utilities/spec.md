## ADDED Requirements

### Requirement: Bessel I0 function
The system SHALL provide a `bessel_i0(x)` function that computes the zeroth-order modified Bessel function of the first kind and returns a float.

#### Scenario: Compute bessel_i0 at zero
- **WHEN** calling `bessel_i0(0.0)`
- **THEN** the result is 1.0

#### Scenario: Compute bessel_i0 at positive value
- **WHEN** calling `bessel_i0(1.0)`
- **THEN** the result is approximately 1.266 (I0(1) ≈ 1.2660658...)

#### Scenario: Function is accessible from top-level
- **WHEN** importing `from pyminidsp import bessel_i0`
- **THEN** the import succeeds and the function is callable

### Requirement: Normalized sinc function
The system SHALL provide a `sinc(x)` function that computes `sin(pi*x) / (pi*x)` with `sinc(0) = 1.0` and returns a float.

#### Scenario: Compute sinc at zero
- **WHEN** calling `sinc(0.0)`
- **THEN** the result is 1.0

#### Scenario: Compute sinc at integer
- **WHEN** calling `sinc(1.0)`
- **THEN** the result is approximately 0.0 (zero crossing)

#### Scenario: Function is accessible from top-level
- **WHEN** importing `from pyminidsp import sinc`
- **THEN** the import succeeds and the function is callable
