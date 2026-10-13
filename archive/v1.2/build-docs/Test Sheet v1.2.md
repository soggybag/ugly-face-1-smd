# Ugly Face 1 SMD v1.2: test sheet

Board: `UglyFace_01` **v1.2** (git tag `v1.2`; `archive/v1.2/` has the schematic PDF and the interactive BOM). LM386 + TLC555, 1590B.
General method: `../../_tools/BENCH_TESTING.md`. The v1.0 results in `Test Sheet.md` are the baseline.

## What's new in v1.2 (what this sheet checks)

| Change | Parts | Check |
|---|---|---|
| THRESHOLD pot → **THR toggle** (ON-OFF-ON) | SW1; RV2 = 3362P 10k trimmer (GLITCH); R7 2k2 to +9V (ON); R8 1k to GND (GATED) | Section 3 |
| **CMOS protection** | R9 22k into U2 pin 4 (RESET); R10 1k between DISCH and C7 | Sections 2 and 4 |
| C5 100µ → 22µ 1206 | envelope coupling | Section 5 |
| New control layout | VOL · FRQ (top), ENV · THR (bottom) | Section 5 |

**Still unprotected on v1.2:** the vactrol LED has no series resistor (ENV at max drives it straight from the LM386). **Fit 100 Ω in the vactrol's LED lead** when you build it (47 Ω if the envelope gets weak). Same as the v1.0 retrofit.

## 0. Before power

| # | Check | Expected | Measured |
|---|---|---|---|
| 0.1 | Visual: U1/U2 pin 1, D1 band, vactrol orientation, SW1 seated, RV2 fitted | as silkscreen | ✅ |
| 0.2 | Ohms J1 (9V) → GND, settle | climbs to tens of kΩ; **fail: a few Ω** | 55.3K ✅ |
| 0.3 | Ohms U2 pin 4 → pin 3 (neighboring pins) | not near 0 Ω | 145K ✅ |

**Section 0 notes (2026-10-09):**
- 0.2 = 55.3k: no short ✓.
- 0.3 = 145k: no bridge between RESET and OUTPUT ✓. That reading is a real circuit path: pin 3 → FRQ pot → DISCH → R3 100k → +9V → R4 22k → THR trimmer → R9 22k → pin 4, ≈ 150–250k depending on the pots.

## 1. First power (100 Ω in series; knobs at noon; SW1 centre; no input)

| # | Check | Expected (v1.0 measured) | Measured |
|---|---|---|---|
| 1.1 | LED off | ~6 mA (0.60 V) | 0.63V = 6.3mA |
| 1.2 | LED on | +~6 mA (R6 1k) | 1.18V = 12mA? |
| 1.3 | Touch U1 and U2 after 1 min | both cool | ✅ |

**Section 1 notes (2026-10-09):**
- 1.2 = 11.8 mA total, so the LED adds **5.5 mA** (v1.0: 5.7) ✓. Idle 6.3 mA ✓; chips cool ✓.
- If this was the 89.9 Ω resistor from the Unit 1 debug, the true values are 7.0 / 13.1 mA (LED +6.1). Either way they're normal, and nowhere near the hot-555 fault (that was +8 mA *while running*).

## 2. DC voltages (no input)

| # | Node | Expected | Measured |
|---|---|---|---|
| 2.1 | +9V (U2 pin 8) | supply − ~0.25 V | 8.73V |
| 2.2 | U1 pin 5 (AMP_OUT) | ~4.4 V | 4.16V |
| 2.3 | U2 pin 5 (CONT) | ⅔ of +9V ≈ 5.9 V | 5.82V |
| 2.4 | **Bias node: SW1 pin 2** (middle pin; also the RV2 trimmer's wiper and C4), then **U2 pin 4**. Both read the same (R9 carries no DC current) | see section 3 | 1.4V / 1.4V |

**Section 2 notes (2026-10-09):**
- +9V 8.73 V ✓.
- CONT 5.82 V = exactly ⅔ × 8.73 ✓.
- Bias node 1.4 V at both SW1 pin 2 and U2 pin 4 ✓: no current into RESET, and R9 isn't open.
- **AMP_OUT 4.16 V vs 4.37 (half-supply):** 0.2 V low (v1.0's chip read 4.41).
  - With pins 1–8 shorted, the LM386's input offset is multiplied by its gain (200), so a few tenths of a volt either way is normal chip-to-chip spread.
  - Effect: the clipped square is slightly asymmetric (a little more swing upward). Harmless.
- 1.4 V on the bias node is above the TLC555's ~1.0 V reset threshold, so with SW1 centre the 555 is probably droning now. Section 3 sets the trimmer.

## 3. THR toggle (the main new feature)

Bias predictions at +9V = 8.8 V, with RV2 set so GLITCH sits at the reset threshold (~1.0 V on the v1.0 chip):

| Position | Adds | U2 pin 4 | Behaviour |
|---|---|---|---|
| GLITCH (centre) | nothing: RV2 alone, range **0.27–2.9 V** | set to **~1.0 V** | on the edge: sputters, fragments |
| ON | R7 2k2 to +9V | **~5.7 V** | drones; playing cuts holes |
| GATED | R8 1k to GND | **~0.23 V** | silent until you play |

1. SW1 centre, no input. Scope on U2 pin 3 (or audio probe on OUT). Turn RV2 until the 555 **just** starts. Read pin 4: that's this chip's reset threshold. Then back RV2 off a hair (just silent) for the "glitch" edge.
2. Flip SW1 each way and read pin 4. **Label which lever direction is ON and which is GATED** (it depends on how the toggle is fitted).

| # | Check | Measured |
|---|---|---|
| 3.1 | Reset threshold (pin 4 where it just starts) | 1.06V |
| 3.2 | Pin 4: GLITCH / ON / GATED | Pin 4: 0.23V / 1.06V / 5.85V |
| 3.3 | Lever direction for ON | 5.85V |
| 3.4 | Any hysteresis (turns on and off at different RV2 settings)? | 1.06V |

**CMOS check (scope, guitar playing hard, GATED):** pin 4 will still dip to about −0.6 V on negative peaks (the chip's internal diode clamps). That's expected. The difference from v1.0 is the **current**: R9 22k limits it to well under 0.5 mA.

## 4. Oscillator (SW1 ON so it drones; no input)

| # | Check | Expected (v1.0 measured) | Measured |
|---|---|---|---|
| 4.1 | U2 pin 3, FRQ at the low end | ~125 Hz, 8.6 Vpp square | 7.3ms 8V |
| 4.2 | U2 pin 3, FRQ at the high end | ~8 kHz, square with sag on the top | 40µS 8V with a small slope at the top |
| 4.3 | U2 pin 7 (DISCH) vs C7 side of R10 | same square; R10 1k barely changes it | Looks about the same at low frequency , at high frequency the wave is blurred on the scope. Looks like a fuzzy slope |
| 4.4 | Supply current, FRQ max vs min | rises ~2–3 mA at max (charging C6) | With the 100ohm resistor (LED off): 1.06V = 10.6mA |

**Section 3 notes (2026-10-09):**
- Reset threshold **1.06 V** (v1.0's chip: 1.0 V) ✓.
- Toggle: GATED **0.23 V** (predicted 0.23) ✓, GLITCH 1.06 V ✓, ON **5.85 V** (predicted ~5.7) ✓.
- No hysteresis (starts and stops at the same 1.06 V) ✓.
- **To do:** note the physical lever direction for ON (e.g. "lever toward VOL"), so the panel can be labelled.

**Section 4 notes (2026-10-09):**
- 4.1 low end: 7.3 ms = **137 Hz**, 8 Vpp (v1.0: 125 Hz) ✓.
- **4.2 high end: 40 µs = 25 kHz, 3× v1.0's 8.3 kHz. Re-check.**
  - The timing resistance can't go below R2 470 Ω (+ the chip's ~400 Ω output). With C6 100n that's ~8–15 kHz.
  - Likely causes: a half-cycle read as a full one, or Time/DIV off its detent.
  - Cross-check from 4.4: the 555's extra current ≈ C6 × V/3 × f. With +4.3 mA (10.6 vs the 6.3 mA idle in 1.1) that gives f ≈ 4.3 mA / (100n × 2.9 V) ≈ **15 kHz**. Higher than v1.0, but not 25 kHz.
  - Ear test: at FRQ max, is there still an audible high whistle? At 25 kHz it would go silent.
- 4.3: the slope / blur on DISCH at high pitch is expected.
  - At the high-pitch end the FRQ wiper sits at the far end from DISCH. DISCH is then pulled up only by R3 100k, so its rising edge is slow (the slope).
  - The "fuzz" is scope trigger jitter on a fast, slightly unstable edge.
  - The result is a softer, rounder top end at high pitch.
- **Re-measured over full cycles:** low end **14 ms = 71 Hz**, high end **70 µs = 14.3 kHz**.
  - Low end matches the formula exactly (0.72 / (100.5k × 100n) = 72 Hz), so C6 really is ~100n.
  - High end: R_eff = 0.72 / (14.3k × 100n) ≈ 500 Ω = R2 470 + only ~30 Ω of chip output resistance. It agrees with the current estimate (~15 kHz).
  - **v1.0's 125 Hz / 8.3 kHz were probably also partial-cycle readings.**
  - Range ≈ 7.6 octaves. The top ~2 octaves (above ~4 kHz) are piercing. If the top of FRQ is unusable, **R2 470 → 1k2** caps it at ~6 kHz (Ugly Face roadmap, phase 0).
- 4.4: also measure the current at FRQ **min** (should be close to 6.3 mA) to get the true difference.

## 5. Signal (guitar)

| # | Check | Expected | Seen |
|---|---|---|---|
| 5.1 | GATED: silent with no playing; bursts per note | yes | ✅ |
| 5.2 | GLITCH: fragments and stutter | yes | ✅ |
| 5.3 | ON: drone, playing cuts holes | yes | ✅ |
| 5.4 | ENV up: pitch rises with playing level, with a slow swoop | yes (with the 100 Ω vactrol resistor fitted) | ✅ |
| 5.5 | Knob directions: VOL, FRQ, ENV increase clockwise | yes | ✅ |

**Section 5 notes (2026-10-09):** everything passes (GATED / GLITCH / ON behaviour, the envelope pitch rise with the 100 Ω vactrol resistor, knob directions).
- Observation: the envelope is strongest on the low E, marginal on A/D, weak on G/B/E. Options for the next version are in `Ugly Face 3 SMD/Ugly Face Roadmap.md` → "Envelope: string balance".

## 6. After boxing

- Supply current again (same as 1.1).
- Cables in before power; don't hot-plug the OUT cable.

## Record

| Item | Result |
|---|---|
| Unit number | 1 |
| Date | 10 09 26 |
| Notes |  |
