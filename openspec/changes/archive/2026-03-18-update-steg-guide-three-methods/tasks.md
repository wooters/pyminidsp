## 1. Guide — Methods Section

- [x] 1.1 Change heading from "Two methods" to "Three methods" in `docs/guides/audio-steganography.rst`
- [x] 1.2 Add STEG_SPECTEXT row to the comparison table (capacity, audibility, robustness, requirements)
- [x] 1.3 Add a paragraph describing how SPECTEXT works (hybrid LSB + spectrogram text art)
- [x] 1.4 Add a `.. seealso::` cross-reference to both the local Spectrogram Text Art guide and the upstream miniDSP C library docs (`https://wooters.github.io/miniDSP/audio-steganography.html`)

## 2. Guide — Code Examples

- [x] 2.1 Add a SPECTEXT encode/decode code example in the "Hiding text" section (or a new subsection)
- [x] 2.2 Update the "Automatic detection" code example to handle `md.STEG_SPECTEXT` as a third case

## 3. API Reference

- [x] 3.1 Update `docs/api/steganography.rst` intro text from "Two methods" to "Three methods" and add SPECTEXT to the comparison table
- [x] 3.2 Update `steg_encode` `:param method:` to list `:data:\`STEG_SPECTEXT\`` alongside LSB and FREQ_BAND
- [x] 3.3 Update `steg_encode_bytes` `:param method:` to list `:data:\`STEG_SPECTEXT\``
- [x] 3.4 Update `steg_detect` description to mention SPECTEXT detection

## 4. Audio & Plot Asset Verification

- [x] 4.1 Verify all three WAV files (`steg_host.wav`, `steg_lsb.wav`, `steg_freq.wav`) are copied to `_build/html/_static/audio/` and playable
- [x] 4.2 Verify both interactive plot iframes (`steg_lsb_diff.html`, `steg_freq_spectrogram.html`) are copied to `_build/html/_static/plots/` and render correctly
- [x] 4.3 Verify the `spectrogram_text_hello.wav` audio and `spectext_hello_spectrogram.html` plot are present if referenced by the updated guide
- [x] 4.4 Check that `raw:: html` relative paths (`../_static/audio/...`, `../_static/plots/...`) resolve correctly from the built `guides/audio-steganography.html` page
- [x] 4.5 If any assets are missing or broken, regenerate by deleting marker files and running `sphinx-build` from the `docs/` directory

## 5. Build Verification

- [x] 5.1 Run `sphinx-build` and confirm no warnings or errors from the changed files
- [x] 5.2 Open the built guide in a browser and confirm all audio players load and all iframe plots render
