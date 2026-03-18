## Context

The Audio Steganography guide (`docs/guides/audio-steganography.rst`) and API reference (`docs/api/steganography.rst`) were written when only two methods existed (LSB and Frequency-band). The `STEG_SPECTEXT` method was added in v0.5.0 but the steganography documentation was never updated to include it. A separate Spectrogram Text Art guide exists (`docs/guides/spectrogram-text.rst`) but it's not cross-referenced from the steganography pages.

The existing `steg_encode`/`steg_decode` functions already accept `method=STEG_SPECTEXT` — no code changes are needed, only documentation updates.

## Goals / Non-Goals

**Goals:**
- Update the guide to document all three steganography methods
- Add SPECTEXT to the comparison table with accurate capacity/audibility/robustness info
- Add a code example showing SPECTEXT usage
- Cross-reference the Spectrogram Text Art guide for deeper detail
- Update the API reference parameter docs to list STEG_SPECTEXT as a valid method
- Fix the detection code example to handle the third method

**Non-Goals:**
- No code changes to any Python or C source
- No new audio samples or plot generation (link to existing spectext assets if available)
- No changes to the standalone Spectrogram Text Art guide

## Decisions

### 1. SPECTEXT description for the comparison table

**Decision**: Describe SPECTEXT as a hybrid method — hides data via LSB encoding while also rendering the message as visible text in a spectrogram view. Capacity and robustness are similar to LSB since it uses LSB as the transport.

**Rationale**: This accurately reflects how the C implementation works (minidsp_spectext.c combines LSB encoding with spectrogram rendering).

### 2. Cross-reference approach

**Decision**: Add a brief description in the guide with a `.. seealso::` directive pointing to both:
1. The local Spectrogram Text Art guide (`docs/guides/spectrogram-text.rst`) for pyminidsp-specific usage
2. The upstream miniDSP C library's steganography docs at `https://wooters.github.io/miniDSP/audio-steganography.html` for the underlying algorithm details and C-level examples

**Rationale**: Avoids duplication, keeps the steganography guide focused on the encode/decode workflow, and connects users to the authoritative C library docs for deeper technical detail on the SPECTEXT method.

### 3. Audio sample for SPECTEXT

**Decision**: Reference the existing `spectrogram_text_hello.wav` audio sample and `spectext_hello_spectrogram.html` plot already generated for the spectrogram text guide, rather than generating new ones.

**Rationale**: Assets already exist; no need to duplicate or regenerate.

## Risks / Trade-offs

- **[Accuracy of SPECTEXT characteristics]** → The capacity/audibility/robustness values for SPECTEXT in the comparison table are inferred from the implementation (LSB-based transport). Verify by testing if needed, but the description should be accurate given it uses the same LSB mechanism.
