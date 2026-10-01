# Ugly Face 1 SMD: build notes and v2 ideas

Findings from bench testing (see `Test Sheet.md` for the measurements).

## THRESHOLD acts like a 3-position switch, not a range (2026-10-01)

- Measured: RESET bias range 0.28–2.63 V; TLC555 reset threshold = **1.0 V**, crossed at ~30% rotation.
- In use, the knob gives **three behaviours** rather than a smooth range:
  1. **Gated:** bias well below 1 V. Silent at idle; the 555 only runs on the guitar's positive swings.
  2. **Glitchy:** bias right at ~1 V. The gate chatters on the edge, giving unstable, broken-up bursts.
  3. **On:** bias well above 1 V. The 555 drones; playing cuts holes in it.
- **v2 idea: replace RV2 with a 3-position switch** (ON-ON-ON toggle, or a SP3T slide/rotary):
  - GATED: RESET biased ~0.3 V (as now at CCW).
  - GLITCH: RESET biased at the threshold. **Make this a trimmer**, because the reset threshold varies from chip to chip (datasheet range; this one is 1.0 V).
  - ON: RESET biased ~2.5–3 V.
  - Keep C4 coupling the guitar onto RESET in all positions. Keep the bias source impedance in the low kΩ so the C4 high-pass (~24 Hz) stays put.
- This frees a panel position (e.g. for a dry/blend or a second oscillator control).

## Other v2 items from testing

- **DISCH output is loaded:** it averages 3.27 V instead of ~4.4 V, because R3 100k pulls up against VOLUME 100k through C7. Lower R3 (≈10k), or take the output from pin 3 (push-pull) through a resistor.
- **FREQUENCY top end limited by the TLC555 output resistance:** R2 470 Ω is comparable to the output's few hundred Ω, so the top is 8.3 kHz, not 15 kHz, and the square sags at CW. Raise R2 (≈1k) for a cleaner top end, or accept it.
- **Vactrol LED has no series resistor** at ENVELOPE max (LED directly on C5 / LM386 output). Check the current in the section 4 tests; add ~100–220 Ω if it's high.
- **FREQUENCY low end:** 125 Hz measured vs ~72 Hz predicted, with 104k measured from pin 3 to pin 2 (so the resistance is fine). Open: C6 value or the scope timebase reading (see the test sheet).
