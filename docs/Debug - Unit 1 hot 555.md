# Ugly Face 1 SMD v1.0: Unit 1, hot 555 / weak output (2026-10-08)

## What happened

- All the v1.0 boards passed a short audio test and went into boxes.
- **Unit 1, re-tested later:**
  - not working;
  - U2 (TLC555) very hot;
  - output very low.
- **After unplugging and re-powering:**
  - The 555 is no longer hot, but the board isn't right.
  - THRESHOLD goes off → crackly middle zone → off.
  - FREQUENCY doesn't reach its full range, and the volume drops past about halfway.
  - ENVELOPE barely does anything; it used to be very pronounced.

## Likely causes (most likely first)

1. **TLC555 latch-up, now partly damaged.**
   - A hot chip with a near-dead output that clears on a power cycle is CMOS latch-up: a parasitic short across the supply inside the chip, triggered when a pin is pulled outside the rails.
   - v1.0 has two unprotected paths into U2 (see `Build Notes.md`, "Protecting the CMOS 555"):
     - **RESET (pin 4)** is driven ~3 V below ground on every guitar cycle, and harder at power-down. C4 2.2µ couples the LM386 output straight onto it, with no series resistor.
     - **DISCH (pin 7)** drives the OUT jack directly through C7. Plugging or unplugging the output cable, static, or the amp's input coupling cap all land on the pin.
   - Latch-up often leaves damage: a leaky input or a weak output transistor. That fits "working but not right".
   - **A weak DISCH transistor explains "volume drops past halfway".** The audio comes from DISCH, which is pulled up by R3 100k and tied to the 555 output through part of RV3.
     - If DISCH can't pull fully low, the low level is set by the divider between that part of RV3 and R3.
     - As FREQUENCY turns, that resistance grows and the swing shrinks.
2. **Vactrol LED overdriven or weakened.**
   - On v1.0 the LED sits directly on C5 / ENVELOPE, with no series resistor.
   - With ENVELOPE up, the LM386 output dumps current into it on every positive half-cycle, plus a pulse at each power-up as C5 charges.
   - A tired LED gives a weak envelope. If the LED went short, it would also overload the LM386.
3. **LM386 damaged** (less likely, but check it).
   - A weak LM386 would weaken both the gate (crackly THRESHOLD) and the envelope at once.
   - If it was the LM386 that was hot rather than the 555, this moves to the top. The two chips are close together.

## Do knob positions at power-up matter?

Not by themselves. The trigger is more likely **plugging and unplugging** (power or cables) on a board that has no protection. Some settings make it worse:

- **ENVELOPE at max:** zero resistance in series with the vactrol LED, so the biggest current pulses (the LM386 is the only limit).
- **THRESHOLD at the low-bias end (~0.3 V):** RESET swings furthest below ground on every note.
- **Hot-plugging the OUT cable while powered:** a transient straight onto 555 pin 7.
- **Unplugging power with the guitar still ringing:** C4 holds its charge while the LM386 output collapses, which drives pin 4 well negative as the supply drops.

## Debug sequence

**Setup:**
- Power through **9 V + 100 Ω in series**, so each 1 mA shows as 0.1 V across the resistor. It also limits current if the board latches again.
- Use one of the boxed boards as a **known-good reference** and measure it alongside. Baseline numbers are from the Oct 1 test sheet.
- Settings: footswitch LED off, knobs at noon unless noted.

| # | Check | Baseline (Oct 1) | Unit 1 now | Good board |
|---|---|---|---|---|
| 1 | Supply current, LED off (V across 100 Ω ÷ 100) | 6.0 mA | | |
| 1b | Feel U1 and U2 after 1 min (which one is warm?) | both cool | | |
| 2 | +9V at U2 pin 8 | 8.8 V | | |
| 3 | U1 pin 5 (AMP_OUT), DC | 4.41 V | | |
| 4 | U2 pin 4 (RESET), THRESHOLD each end | 0.28 V / 2.63 V | | |
| 5 | U2 pin 5 (CONT) | 5.86 V | | |
| 6 | U2 pin 3, scope, THRESHOLD at drone end | 8.6 Vpp square | | |
| 7 | U2 pin 7, scope, same | low level ~0 V, high ~6.5–7 V | | |
| 8 | Pin 3 frequency, FREQUENCY CCW / CW | 125 Hz / 8.3 kHz | | |
| 9 | Pin 7 swing at FREQUENCY ¾ (compare with pin 3) | about full swing | | |
| 10 | AMP_OUT with guitar / 200 mVpp sine, scope | 7–8 Vpp clipped square | | |
| 11 | Vactrol, power off: ohms across LDR (U3 3–4), covered | MΩ range | | |
| 12 | Vactrol, power off: diode test on the LED (red on U3 pin 1) | ~1.6–2.0 V | | |
| 13 | Vactrol: light the LED (9 V + 1k into U3 pin 1, pin 2 to GND) and read the LDR | drops to ~1k or less | | |

**How to read it:**

- **Step 1 well above 6 mA** (or a chip warms up): something is still partly shorted. Note which chip is warm.
- **Step 4 top end well below 2.63 V:** pin 4 is now leaky. The input protection is damaged, so the 555 can't be biased past its ~1.0 V reset threshold. That fits THRESHOLD going "off" at both ends. **Replace U2.**
- **Steps 7/9: pin 7 doesn't pull close to 0 V,** or its swing shrinks as FREQUENCY turns while pin 3 stays a full square: the DISCH transistor is weak. **Replace U2.**
- **Step 6/8: pin 3 is smaller than 8.6 Vpp, its edges sag badly, or CW tops out well below 8.3 kHz:** the output stage is weak. **Replace U2.**
- **Step 10 low or misshapen** (and the input is good): the LM386 is damaged. Replace U1 (LM386MX-1).
- **Steps 11–13:**
  - LED reads open or short: the vactrol LED is dead.
  - LDR doesn't drop when the LED is lit: the LED is weak.
  - Either way, **rebuild the vactrol.**

For a quick A/B on any single node, probe the same point on the good board.

## Fix and retrofit (Unit 1, then the boxed boards)

**Replace what tested bad.** U2 TLC555IDR (SOIC-8, LCSC C6987); ICM7555 SOIC also fits. U1 is LM386MX-1 if needed. Rebuild the vactrol if needed.

Then add the v1.2 protection, so it doesn't happen again. All three are small reworks:

1. **22k in series with RESET:**
   - Lift U2 pin 4 off its pad (heat the pin, lever it up gently with a blade).
   - Solder a 22k 0805 from the lifted pin down to the pad.
   - RESET draws almost no current, so the sound and THRESHOLD don't change. The clamp current drops from tens of mA to under 0.5 mA.
2. **1k in series with the output:**
   - Lift C7's DISCH-side end (tombstone it).
   - Bridge the gap with a 1k 0805 (or a 1/4 W leaded resistor).
   - This puts 1k between the OUT jack and pin 7.
3. **Series resistor in the vactrol LED leg:** 100 Ω to start; 47 Ω if the envelope gets too weak.
   - The vactrol is hand-built, so the resistor can go in the LED's anode lead with no board rework.
   - It stops ENVELOPE-at-max dumping the LM386 output into the LED.

**Habits until the boards are modded:**
- Plug cables before power.
- Turn ENVELOPE down before powering up.
- Don't hot-plug the OUT cable.

Record the outcome in `docs/Build Log.md` (Unit 1) and add the retrofit to each boxed board's entry.

## Results, Unit 1 (2026-10-08)

Setup: 9 V through 89.9 Ω (measured), no input, LED off unless noted.

| Reading | Value | Current | Notes |
|---|---|---|---|
| LED off (knobs noon) | 0.83 V | 9.2 mA | Oct 1 baseline 6.0 mA at 8.8 V |
| LED on | 1.35 V | 15.0 mA | LED adds 5.8 mA (baseline 5.7): fine |
| U2 pin 8 | 7.12 V | | supply sag through the 89.9 Ω |
| U2 pin 4, THRESHOLD max | 2.12 V | | 2.12 / 7.12 = **0.298**, Oct 1 2.63 / 8.8 = 0.299 → **RESET not leaky** |
| A. THR silent end, FREQ noon | 0.87 V | 9.7 mA | 555 held in reset |
| B. THR silent end, FREQ CCW | 0.87 V | 9.7 mA | = A, as expected |
| C. THR drone end, FREQ CCW | 1.63 V | 18.1 mA | **+8.4 mA as soon as the 555 runs** |
| D. THR drone end, FREQ CW | 1.59 V | 17.7 mA | same as C: the extra doesn't depend on frequency |

**Reading:**
- Normal 555 switching current rises with frequency (about 2.9 mA at CW on Oct 1, near zero at CCW). Here the 555 adds a **steady ~8 mA whenever it runs, at any frequency**.
- That's a DC fault inside the chip, consistent with a latch-up-damaged output or discharge stage that partly conducts in one output state (shoot-through) on every cycle.
- Even in reset (A), the board draws ~9.7 mA at 7.1 V, where a healthy board would be ~5 mA. Something else is also drawing extra: 555 leakage, or the LM386.

**Verdict: replace U2.** Then repeat A–D. If A is still high, check the LM386 next: is it warm, and does pin 5 show HF oscillation on the scope?

## Retrofit without lifting pins (2026-10-09)

Lifting U2 pin 4 isn't practical: the SOIC legs are ~1 mm and would break. Do it with THT parts on the pots and the wiring instead:

1. **RESET: Schottky clamp from the THRESHOLD wiper lug to ground.**
   - Use a BAT43, BAT85 or BAT46 (Tayda has BAT43 / 1N5817). Cathode (band) on the THRESHOLD pot's middle lug (RV2 pin 2 = RESET), anode to ground.
   - For ground, run a short insulated lead to the nearest ground pad (J2 9V GND, or J4 / J6). Don't use THRESHOLD's own end lug: that sits on R5 1k, not ground.
   - The Schottky conducts at ~0.3 V, before the 555's internal diode (~0.6 V), so it carries nearly all the negative-swing current. The internal diode current drops by orders of magnitude.
   - The sound barely changes. The negative peaks are now caught at −0.3 V instead of −0.6 V, which shifts the THRESHOLD sweet spot slightly.
   - Same idea as the v1.2 notes' optional "BAT54S clamp".
2. **Output: 1k in the OUT wire** between header J3 pin 4 and the output jack tip (heat-shrink it in the wire). That puts 1k + the VOLUME pot between the jack and 555 pin 7, so no board rework is needed.
3. **Vactrol: 100 Ω in the LED lead** (47 Ω if the envelope gets weak).

Do these on the boxed boards too; they don't need a replacement 555.
