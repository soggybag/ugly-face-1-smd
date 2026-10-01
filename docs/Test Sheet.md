# Ugly Face 1 SMD: test sheet

Gear: multimeter, oscilloscope, audio probe. Expected values are hand calculations (see `Circuit Walkthrough.md`).
Record the supply voltage first. Every expected value scales with it.

## 0. Before power

| Check | Expected | Measured | OK |
|---|---|---|---|
| Visual: U1/U2 pin-1 dots, D1 band, C5 polarity, vactrol LED orientation | as silkscreen | - | x |
| Short check: ohms, red on J1 (9V pad), black on GND | starts low and climbs while C1 charges, then settles at tens of kΩ or more. **Fail: near 0 Ω or a steady few Ω** | 4K | x |
| Same with the leads swapped (black on J1) | OL / very high (D1 blocks) | - | x |
| Short check: ohms, red on +9V (D1 cathode), black on GND | climbs, then settles at tens of kΩ (the 33k THRESHOLD divider in parallel with the ICs) | 27K | x |
| D1 diode test (red on J1, black on cathode) | 0.15–0.3 V | 200mv | x |

## 1. First power (no input, footswitch off, all knobs at noon)

Use a current-limited supply, or 9 V through a 100 Ω resistor (each 1 mA shows as 0.1 V across it).

| Check | Expected | Measured | OK |
|---|---|---|---|
| Supply voltage at J1 | ~9.0–9.6 V | 7.94V | x |
| Current draw, LED off | **~5 mA** (LM386 ≈ 4 mA + dividers) | 0.6v | x |
| Current draw, LED on (LED_K to GND) | **~11–12 mA** (+ ~7 mA LED) | 1.17V | x |
| Current with FREQUENCY at max pitch and the gate open | rises a few mA (555 driving C6 through 470 Ω) | 1.46V | x |

## 2. DC voltages (black probe on GND)

| Node | Where | Expected | Measured |
|---|---|---|---|
| +9V | D1 cathode / U1 pin 6 / U2 pin 8 | supply − 0.2–0.3 V | 8.8V |
| LED anode (LED on) | D2 + / R6 | ~2 V (red) | 1.96V |
| U1 pin 3 (+in) | | ~0 V | 0.01V |
| U1 pin 5 (AMP_OUT) | | **~4.5 V** (pins 1–8 shorted: may be off by up to ~1 V; note it) | 4.41V |
| U1 pin 7 (bypass) | | a few volts (record) | 4.44V |
| U2 pin 4 (RESET), THRESHOLD full CCW | | ~0.27 V *or* ~3.0 V (depends on pot orientation) | 2.63V |
| U2 pin 4 (RESET), THRESHOLD full CW | | the other end: ~3.0 V / ~0.27 V | 0.28V |
| U2 pin 5 (CONT) | | **6.0 V** (⅔ V+) | 5.86V |
| U2 pins 2/6 (TIMING), 555 running | | ~4.5 V average (DMM); scope: 3 V ↔ 6 V | 4.41V |
| U2 pin 3 (OSC_SQ), running / held in reset | | ~4.5 V avg / 0 V | 4.45V |
| U2 pin 7 (DISCH), running / held in reset | | ~4.5 V avg / 0 V | 3.27V |
| Vactrol LED anode (no signal) | RV1 wiper | 0 V | 0V |

## 3. Experiment: find the TLC555 reset threshold

1. No input. Scope (or audio probe) on OUT or U2 pin 3.
2. Turn THRESHOLD slowly from the low-voltage end until the 555 **just starts** oscillating.
3. Measure U2 pin 4 at that point. **That's the real reset threshold** (expected ~1 V; the datasheet allows a range).

| Reset threshold (V) | |
|---|---|
|  | 1V |

## 4. Signal tests (scope; guitar or a ~200 mVpp 200 Hz sine into IN)

| Point | Expected | Seen |
|---|---|---|
| U1 pin 5 (AMP_OUT) | clipped square, ~7–8 Vpp around ~4.5 V (note the symmetry) | |
| U2 pin 4 (RESET) | the same square, AC-coupled, centred on the THRESHOLD bias | |
| U2 pins 2/6 (TIMING) | exponential ramps 3 ↔ 6 V; restarting from 0 V each time the gate opens (sync) | |
| U2 pin 7 / OUT | 555 square bursts, gated per guitar cycle | |
| FREQUENCY min / max (gate held open, no LDR light) | ~72 Hz / several kHz (record the actual values) | 125 Hz to 16.7 kHz |
| Vactrol LED anode, ENVELOPE max, strong signal | positive half-cycles ~1.8–2 V (LED clamps) | |
| Pitch change with playing level (ENVELOPE up) | louder → higher pitch, with a slow swoop | |

**Vactrol LED drive check:** put the 100 Ω series resistor (from section 1) in series with the supply and compare the current with ENVELOPE at 0 vs max under a strong signal. A large jump (tens of mA) means the LED is being driven hard; we'd then add a series resistor in v2.

## 5. Audio probe trace (cap-coupled probe, low volume)

IN → U1 pin 3 → U1 pin 5 (loud fuzz) → U2 pin 4 (gated fuzz) → U2 pin 3 (synth tone) → OUT (volume-scaled).

## Notes / surprises

- **Section 1 (2026-10-01):** idle 6.0 mA, LED +5.7 mA, 555 at max pitch +2.9 mA.
  - From I = C·ΔV·f, the 555's extra current predicts the max-pitch frequency: f ≈ 2.9 mA / (100n × 2.6 V) ≈ **11 kHz**. Verify on the scope.
- **U1 pin 5 = 4.41 V with +9V = 8.8 V**, which is exactly V+/2. Shorting the LM386's pins 1 and 8 directly did *not* shift the bias on this chip. The predicted offset didn't appear.
- **THRESHOLD range 0.28–2.63 V (predicted 0.27–2.93 V at 8.8 V).** Solving 8.8·(1k + P)/(23k + P) = 2.63 gives **RV2 ≈ 8.4k**, within the ±20% tolerance of a 10k pot. The bottom end (8.8·1k/31.4k = 0.28 V) agrees.
- **CONT 5.86 V** = ⅔ × 8.8 ✓. **TIMING 4.41 V** = midpoint of 2.93 ↔ 5.87 ✓. **OSC_SQ 4.45 V** ≈ 50% duty ✓.
- **DISCH 3.27 V (expected ~4.4 V): this is loading.**
  - DISCH only pulls *down*. Going high, it is pulled up by R3 100k (in parallel with part of the FREQUENCY pot), against VOLUME's 100k load through C7.
  - That divider stops the output square reaching the full 8.8 V. The high level comes out at roughly 6.5–7 V, so the average is ~3.3 V.
  - Prediction: the DISCH average changes with the FREQUENCY setting (stronger pull-up when the wiper is near pin 1). Scope DISCH to see the reduced high level.
  - v2 idea: lower R3 (e.g. 10k), or take the output from pin 3 (push-pull) through a resistor.

- **Oscillator range (scope on U2 pin 3, 8.6 Vpp square):**
  - FREQUENCY CCW: 4 div × 2 ms = 8 ms, **125 Hz** (predicted ~72 Hz).
  - FREQUENCY CW: 12 div × 10 µs = 120 µs, **8.3 kHz** (predicted ~15 kHz with only R2 470 Ω).
  - **CW runs slow:** the TLC555 output has a few hundred Ω of internal resistance, which adds to R2. R_eff = 0.72 / (8.3k × 100n) ≈ 870 Ω, so the output is ≈ 400 Ω. Check: the square's top and bottom should sag visibly at CW.
  - Section 1 current cross-check: C·ΔV·f = 100n × 2.6 V × 8.3 kHz ≈ 2.2 mA vs 2.9 mA measured, so that method agreed better than first thought.
  - **CCW runs fast:** the effective timing R ≈ 0.72 / (125 × 100n) ≈ 58k instead of 100.5k.
    - Covering the vactrol made no change, so it's not room light reaching the LDR.
    - Suspects: the LDR's *dark* resistance (it may be only ~100–200k), a low-reading RV3, or C6 under value.
    - Next test: power off, FREQUENCY CCW, ohms from U2 pin 3 to U2 pin 2. Expect ~100k if nothing is in parallel.
- **TLC555 reset threshold = 1.0 V** (section 3).
  - On THRESHOLD: 8.8 × (1k + x) / 31.4k = 1.0 gives x ≈ 2.6k of the 8.4k track, so the gate opens at about **30% rotation**.
  - Below that it idles closed (silent until you play); above it, it drones.
- **U2 pin 3 → pin 2, power off, FREQUENCY CCW: 104k** (RV3 + R2 ≈ 100.5k expected). So the timing resistance is right, and neither the LDR nor anything else is in parallel.
  - The fast low end must then come from **C6** (125 Hz would imply C ≈ 0.70 / (125 × 104k) ≈ 54n) **or the CCW timebase reading** (the Time/DIV knob was between detents earlier).
  - To do: re-time CCW with the knob clicked in (or a tuner app on OUT: 72 Hz ≈ D2, 125 Hz ≈ B2), then measure C6 in capacitance mode.
- **CW square shows sag on the top**, confirming the TLC555's output resistance.
