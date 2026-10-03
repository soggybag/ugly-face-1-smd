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

## Protecting the CMOS 555 (2026-10-02)

The user has had 7555s die occasionally in past builds. CMOS inputs are damaged by being pulled **outside the supply rails** (below GND or above V+). Each pin has internal protection diodes to the rails. When one conducts, current is injected into the chip's substrate, which can trigger **latch-up**: a parasitic short across the supply that burns the chip unless the current is limited. Limits: inputs from −0.3 V to V+ + 0.3 V; supply ≤ 18 V (TLC555 / ICM7555).

**Where this board can do that (most likely first):**

1. **RESET (pin 4) is driven below ground on every guitar cycle.**
   - The fuzz stage swings about ±3.5 V around its bias and is AC-coupled (C4 2.2µ on UF1, C9 on UF3) onto a RESET bias of only 0.1–2.6 V. The negative half pushes pin 4 down to about −3 V.
   - The pin's internal diode to GND clamps it at about −0.6 V. The current is limited only by the fuzz stage's output (tens of mA). That's substrate injection every cycle.
   - **Worst at power-down / unplugging:** the coupling cap still holds its charge while the fuzz output falls to 0 V, driving pin 4 several volts negative.
   - The clamp also *rectifies*: C4/C9 charge until the negative peaks sit at −0.6 V, which shifts the effective gate bias. That's part of how THRESHOLD actually behaves.
2. **UF1 only: DISCH (pin 7) drives the output jack** through C7 100n and VOLUME, with no buffer. A static zap or plugging transient on the OUT jack goes straight to the 555 pin. (UF3 is safe here: U1B buffers the output and R18 100 Ω isolates it.)
3. **Power-down:** C10/C6 (timing) and the other caps on 555 pins discharge back into the pins as V+ collapses. This is small energy, normally fine.
4. **Supply over-voltage:** SS14 protects against reverse polarity only. A 12–18 V adapter is within the 555's 18 V limit, but **UF1's LM386 is only rated to 15 V** (the TL072 on UF3 is fine).

**Precautions for the next revision:**

- **Series resistor into RESET: 10k–47k between the bias/coupling node and pin 4.**
  - RESET draws only pA, so the bias and the sound don't change.
  - The clamp current drops from tens of mA to < 0.5 mA.
  - This is the single most useful fix. One 0805 resistor.
- **Optional Schottky clamp** (BAT54S, one diode to GND and one to V+) on the node *before* that resistor, so the external diode takes the current instead of the chip.
  - Note: clamping is already happening inside the chip, so this keeps today's sound (the same −0.3 to −0.6 V DC-restore). It just moves the stress outside.
- **UF1: don't drive the jack from the 555 directly.** Add ~1k in series at minimum, or buffer it as UF3 does.
- **Optional over-voltage TVS** across the supply after D1 (e.g. SMAJ15A, or a 15 V zener with the SS14 acting as the series element), mainly for UF1's LM386.
- **Prefer the TLC555 (TI LinCMOS)** over generic ICM7555 clones; keep the 100n at pin 8 close to the chip (already done).
- Both boards already have the C11 10n on CONT, decoupling at pin 8, and series reverse-polarity protection.
