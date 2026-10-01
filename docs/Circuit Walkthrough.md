# Ugly Face 1 SMD: circuit walkthrough

Board: LM386 + TLC555 version (`UglyFace_01.kicad_sch`, rev 1.1). Refs and values are from the KiCad schematic.
Numbers marked *calc* are hand calculations; confirm them on the bench (see `Test Sheet.md`).

## The big picture

```
IN ─► LM386 (gain 200, hard clipping) ─┬─► 
C4 ─► 555 RESET (gate)   ◄── THRESHOLD sets the bias
                                       └─► C5 ─► ENVELOPE ─► vactrol LED ─► LDR across the 555 timing R
555 astable (FREQUENCY) ─► DISCH ─► C7 ─► VOLUME ─► OUT
```

The guitar never reaches the output. What you hear is the **555's square wave**, which the guitar does three things to:
1. **Gates it.** The clipped guitar signal drives the RESET pin, so the 555 is switched on and off *every guitar cycle*.
2. **Restarts (syncs) it.** Each reset discharges the timing cap, so every time the gate opens the oscillator starts a fresh cycle. That's hard sync to your note, and a lot of the "ugly" character.
3. **Bends its pitch.** The louder you play, the brighter the vactrol LED, the lower the LDR resistance, and the higher the 555 frequency.

---

## Block 1: power and LED

- J1 9V → **D1 SS14** (series Schottky, reverse-polarity protection) → +9V. C1 22µ bulk, C8/C9 100n decoupling at each IC.
- **D2 LED**: +9V → R6 1k → D2 → J3 pin 2 (LED_K) → footswitch to ground.

**Ohm's law: LED current** *calc*
- I = (V+ − V_LED) / R6 = (9.0 − 2.0) / 1k ≈ **7 mA** (for a red LED; ~3 V for blue/white gives ~6 mA).
- The SS14 drops only ~0.2–0.3 V at these currents. That's why a Schottky is used instead of a 1N4001 (~0.7 V).

## Block 2: input and LM386 fuzz

- IN → R1 1M pull-down (stops pops from the coupling cap's DC) → C2 1n to GND (RF filter) → **C3 100n** → U1 pin 3 (+). Pin 2 (−) to GND.
- **U1 pins 1 and 8 are tied directly → gain 200 (46 dB).** C10 10µ on pin 7 (bypass, improves supply rejection).

**What to know about the LM386**
- Inputs are referenced to ground internally through **50k**, so no bias resistors are needed.
- The output idles near **V+/2 ≈ 4.5 V**.

**Input high-pass (C3 with the 50k input resistance)** *calc*
- f = 1 / (2π · R · C) = 1 / (2π · 50k · 100n) ≈ **32 Hz**. The full guitar range passes.

**Gain and clipping** *calc*
- A guitar note of ~100 mV peak × 200 = 20 V peak, far beyond the ~±4 V the output can swing on 9 V.
- So **the LM386 is always hard-clipped:** its output is a near-square copy of your note, about 7–8 Vpp around 4.5 V.
- Shorting pins 1 and 8 *directly* (instead of through a 10µ cap, as the datasheet shows) also raises the **DC** gain. Input offset gets multiplied by 200, so pin 5 may sit noticeably off 4.5 V. That makes the clipping asymmetric. **Measure it**: it's a good real-world lesson.

## Block 3: the gate (THRESHOLD → 555 RESET)

- AMP_OUT → **C4 2.2µ** → RESET node (U2 pin 4).
- RESET is biased by a divider: **+9V → R4 22k → RV2 THRESHOLD B10k → R5 1k → GND**, with the wiper on RESET.

**Divider range** *calc*: V = 9 V · (R below the wiper) / (total 33k)
- Wiper at the R5 end: 9 · 1k / 33k = **0.27 V**.
- Wiper at the R4 end: 9 · 11k / 33k = **3.0 V**.

**How the gate works**
- The TLC555 is held in reset while pin 4 is below its reset threshold (around 1 V; the datasheet gives a range). Above it, the 555 runs.
- THRESHOLD sets the *idle* bias relative to that threshold. The clipped guitar square then pushes RESET above and below it, once per guitar cycle.
  - **Bias well below the threshold:** only the guitar's positive half-cycles open the gate, giving short bursts. The gate is closed when you're not playing.
  - **Bias above the threshold:** the 555 runs all the time (drone), and the guitar's negative half-cycles cut holes in it.

**Gate-coupling high-pass (C4 into the divider's Thevenin resistance)** *calc*
- The divider's source resistance at the wiper is roughly 1k–8k depending on the setting, so f ≈ 1 / (2π · 3k · 2.2µ) ≈ **24 Hz**. The note's fundamental passes.

## Block 4: the envelope (ENVELOPE → vactrol)

- AMP_OUT → **C5 100µ** → RV1 ENVELOPE B1k (pin 3; pin 1 to GND). The wiper drives the **vactrol LED** (U3 pins 1/2) directly.
- The **LDR** (U3 pins 3/4) connects from the 555 output (OSC_SQ) to the timing node, **in parallel with the FREQUENCY resistance**.
- So, while you play:
  1. The positive peaks light the LED, and the LDR resistance drops (from MΩ in the dark to around 1k when bright).
  2. That raises the 555 frequency: louder means higher pitch.
  3. The LDR is slow (tens of ms), so the pitch **swoops** rather than tracking each cycle.
- **Watch-out:** with ENVELOPE at maximum, the LED sits right on C5 with no series resistor, so the only current limit is the LM386's output. Check on the bench that the LED isn't being overdriven (see the test sheet).

## Block 5: the 555 oscillator (FREQUENCY)

- TLC555 (CMOS) in the **"output-driven RC" astable**: the 555's own output (pin 3) charges and discharges **C6 100n** through *(RV3 FREQUENCY between its wiper and pin 3) + R2 470*. Pins 2 and 6 watch the cap. C11 10n decouples CONT (pin 5).
- The cap swings between **⅓ and ⅔ of V+** (3 V ↔ 6 V). Each half-cycle takes R·C·ln 2.

**Frequency** *calc*: f = 1 / (2 · ln 2 · R · C) ≈ 0.72 / (R · C), giving a near-50% square wave.
- R max = 100k + 470: f ≈ 0.72 / (100.5k · 100n) ≈ **72 Hz**.
- R min = 470: f ≈ 0.72 / (470 · 100n) ≈ **15 kHz** (in practice the output's current limit softens the top end).
- **The LDR in parallel lowers R:** for example, a 10k LDR across 50k gives 8.3k, which takes the pitch from ~144 Hz to ~870 Hz.
- RV3 is a **C taper (reverse log)**, which spreads the musical range more evenly across the rotation.

## Block 6: output (DISCH → VOLUME)

- The output is taken from **DISCH (pin 7)**. It's an open-drain switch that pulls low whenever the output is low. R3 100k pulls it up when it's off, so DISCH is a 0–9 V square in step with the output.
- → **C7 100n** → **RV4 VOLUME A100k** → OUT.

**Output high-pass** *calc*
- f = 1 / (2π · 100k · 100n) ≈ **16 Hz**.

**Level** *calc*
- A 9 Vpp square is about **4.5 V RMS (+15 dBu)**, far hotter than a guitar.
- That's why VOLUME is an A (log) taper, and why most of the useful range is at the low end of the knob.

---

## Exercises (try before reading the answers above)

1. LED current with a 9.5 V supply and a 2 V LED, through R6 1k (plus the SS14 drop).
2. The RESET voltage with THRESHOLD at mid-travel (5k on each side of the wiper).
3. If C6 were 47n instead of 100n, what would the FREQUENCY range become?
4. The guitar into the LM386 has a ~32 Hz high-pass. What would change if C3 were 10n?
5. Why does the output need C7 at all? (Hint: what DC voltage does DISCH sit at on average?)













