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
- **4 controls vs UF3's 5 (2026-10-02):** after playing both, UF1's four knobs (ENV, THR, FRQ, VOL) may be the better layout than UF3's five (UF3 adds MIX).
  - Idea for the next UF1-style revision: keep it at **four controls total**, with THRESHOLD as a **3-position toggle** (GATED / GLITCH / ON) instead of a pot.
  - That gives three knobs + one toggle: a simpler panel, and the switch matches how THRESHOLD actually behaves.

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

## v1.2 (2026-10-02): THR toggle, CMOS protection, name on silk, new control layout

v1.1 (received from JLC) is tagged `v1.0` in git.

- **Controls (outside view):** top row **VOL · FRQ**, bottom row **ENV · THR**. These are the same four positions as v1.1 (16 mm pots, same drilling); VOL/FRQ/ENV were swapped into place.
- **THR is now a mini toggle** (SW1, Taiway 100 SPDT **ON-OFF-ON**, back side, hand-soldered) on the RESET bias node:
  - centre = **GLITCH**: RV2 is now a **10k trimmer** (Bourns 3362P single-turn cermet, top adjust, hand-soldered, top side; was 3296W multi-turn) in the R4 22k / R5 1k divider. Set it once so the 555 just starts (pin 4 ≈ the chip's reset threshold, ~1.0 V on the bench unit).
  - one throw = **ON**: adds **R7 2k2** to +9V (bias ≈ 5.5 V; drones, playing cuts holes);
  - other throw = **GATED**: adds **R8 1k** to GND (bias ≈ 0.25 V; silent until you play).
  - Which lever direction is ON vs GATED depends on how the toggle is fitted. Label the panel after a quick test.
- **CMOS protection:**
  - **R9 22k** between the bias node and U2 pin 4. It limits the current that drove pin 4 to −0.75 V.
  - **R10 1k** between DISCH and C7, so the output jack no longer connects straight to a 555 pin.
- **C5 100µ electrolytic → 22µ 1206 X5R** (C12891). Needed for space (the toggle took its spot). Into ENV 1k it's ~16 Hz even with DC-bias derating, so the envelope is unaffected.
- **Silkscreen:** "UGLY FACE v1.2" and "SUPER-FREQ" on the front. ${Label} texts THR and GLITCH added.
- U3 pad 2 (vactrol GND) set to no zone connection, to remove a starved-thermal island (it's connected by a track).
- Re-routed. DRC: 0 errors, 0 unconnected (silkscreen warnings only). ERC: only the pre-existing LM386 gain-pin note. Connectivity identical to the schematic.
- **Drill:** `enclosure/UglyFace1_1590B_drill.csv` + SVG (Tayda coordinates; footswitch and jacks not included).
- **JLC files generated 2026-10-02 23:4x** after the user's silkscreen pass: schematic vs board fields 0 mismatches; 24 SMD placements (all top), every LCSC number proven on earlier boards. Fixed while generating: the pots, LED, vactrol, toggle, trimmer and wire pads were still marked "in BOM" (also true in v1.1). Now excluded from BOM and CPL in both schematic and board.
- Optional items from the list above still open: R3 100k → 10k (DISCH loading), R2 470 → 1k (top end), C6 film/C0G (timing-cap derating), vactrol LED series resistor.
- **CMOS latch-up: Schottky clamp at pin 4 (2026-10-13): to be bench-tested on an existing board.**
  - The ICM7555 datasheet limit is **VDD + 0.3 V / GND − 0.3 V** on any pin. Beyond that, the internal protection diodes conduct and can trigger destructive latch-up. It also warns against inputs applied before the supply is up (guitar/amp connected with the pedal unpowered).
  - **v1.2's R9 22k** limits the current (< ~0.5 mA), which makes latch-up much less likely. But pin 4 still dips to ~−0.6 V on hard picking (the internal diode does the clamping), so it's still outside the rated range.
  - **Idea:** a **BAT54S** (or BAT43 to GND, plus one to +9V) at the **pin side of R9** (between R9 and U2 pin 4). At R9's small current, a Schottky drops ~0.2–0.25 V, so pin 4 stays inside −0.3 V and the internal diode never conducts. R9 still limits the current. (This replaces the earlier note that put the clamp *before* R9.)
  - **Both diodes matter (2026-10-13):** in ON mode, the bias (~5.5 V) plus the preamp swing can push pin 4 above +9 V too, so clamp to +9V as well as GND. A BAT54S does both. Retrofit on a built v1.2: two leaded Schottkys (BAT43/BAT85) at R9's pin-4-side pad, one cathode-to-pin-4 with anode to GND, one anode-to-pin-4 with cathode to +9V (pin 8 or its decoupler).
  - **Test:** fit on an existing board. Scope pin 4 while picking hard in GATED (expect negative peaks at ~−0.25 V instead of ~−0.6 V). Listen for any change in THRESHOLD/gate behaviour, since the DC-restore level shifts slightly. Then decide on the next-revision fix.
  - **Result, first board (2026-10-13):** two BAT43s fitted (package: Vf 289 mV, IR 0.37 µA), cathode R3 pin 1 (+9V) → anode R9 pin 2; cathode R9 pin 2 → anode GND. Ohms: R9 pin 2–GND 3.9k, +9V–GND 11.9k (no shorts).
    - Scope at 0.2 V/div, GATED, picking hard: pin 4's bottom flattens at **~−0.2 V** (was ~−0.6 V without the clamp). Inside the −0.3 V rating ✓.
    - GATED peaks reach ~6 V, so the upper diode is idle there.
    - **ON position: the tops flatten at ~9 V** (2 V/div), so the upper diode clamps too ✓. That confirms ON really does push pin 4 above the supply without it.
    - **Listening: little or no audible difference** in any THRESHOLD position ✓.
    - **Decision: adopt it.** Retrofit the other v1.2 boards the same way. Next revision: a BAT54S (C19726, SOT-23, both diodes) at the pin-4 side of R9, common pin on RESET.
- **Vactrol LED series resistor (2026-10-12): value still open, being A/B tested on built units.**
  - 100 Ω (in the LED lead) works but changes the envelope response.
  - 51 Ω was tried on another build.
  - The user will A/B the two and pick a value. **Next revision:** put it on the board as an 0805 (e.g. R11) in the U3 LED path, alongside the unreleased switch-slot footprint change.

## Choosing the LDR / vactrol (2026-10-09)

**How it's used:** the LDR (U3 pins 3–4) sits across the 555 timing resistance: OSC_SQ → (RV3 portion + R2 470 Ω) → C6 100n. That resistance runs from ~470 Ω (FRQ high) to ~100k (FRQ low).
- The LED is driven from the LM386 through C5 and ENV (fit 100 Ω in its lead). That gives current pulses of up to ~15–20 mA with the 100 Ω.

**Spec to aim for:**

| Property | Target | Why |
|---|---|---|
| Dark resistance | ≥ 1 MΩ (≥ 10 MΩ better) | No pitch shift at rest, even at FRQ low (100k) |
| Lit resistance at ~10–20 mA | ≤ ~1 kΩ | Can pull the timing resistance well down: big pitch sweeps |
| Slope (how gradually R follows LED current) | **shallow** (VTL5C9 ≈ 7 vs VTL5C3 ≈ 20) | Pitch follows playing level over a wide range instead of switching; part of the "animation" |
| Decay | ~50–200 ms (VTL5C9: 50 ms to 100k) | The swoop after each note. Slow parts (VTL5C4, ~1.5 s) give long glides; fast ones are twitchier |
| LED current rating | ≥ 20 mA continuous | Peaks with ENV at max |

**VTL5C9 (the reference that sounds good):** ~630 Ω at 2 mA, 50 MΩ dark, slope 7.3, 112 dB range, 4 ms on, 50 ms decay to 100k. Its wide dynamic range and shallow slope are why the envelope sounds animated.

**DIY LED + CdS cell:**
- CdS is most sensitive to green/yellow-green light, so a green or bright white LED couples better than red.
- The GL55xx family (5516 → 5549) goes from low lit / low dark resistance to high lit / high dark resistance. 5528–5539 are a good middle.
- Seal the pair light-tight.

**Quick sort of a box of parts:**
1. Meter on the LDR. Light the LED from 9 V through 8k2 / 1k5 / 470 Ω (~1 / 5 / 15 mA for a red LED) and note R at each.
2. Then remove the LED current and time roughly how long R takes to pass ~100k.
3. Compare with a VTL5C9 measured the same way. A similar curve should give a similar feel.

## Build note (2026-10-09): THR toggle pins too big for the holes

**Found while building v1.2:** the Taiway 100 toggle's pins don't fit SW1's holes (1.3 mm round drill).

Caliper measurements:

| Terminal | Measured | Diagonal | Fits a 1.3 mm hole? |
|---|---|---|---|
| PCB pins | 1.29 × 0.74 mm | 1.49 mm | no |
| Solder lugs | 2.22 × 0.71 mm | 2.33 mm | no |

**For this v1.2 build (safest first):**
1. **Wire it:** mount the toggle in the enclosure and run three short wires from its lugs to SW1's pads. No board damage.
2. **Narrow the PCB pins:** file the pins' width down until they enter the 1.3 mm holes, then solder normally.
3. **Last resort, drilling the holes to 1.5 mm:** this cuts away the hole plating that joins the two copper sides. Solder each pin on both sides, and check continuity from each pad's top-side track to its bottom-side track.

**Fixed for the next revision (unreleased, after v1.2):**
- `UglyFace:SW_Taiway_100_SPDT_PC` now has **plated oval slots 2.6 × 1.1 mm**, pads 3.4 × 2.2 mm (pin 1 still rectangular). The **4.70 mm pitch is unchanged**. It takes either the solder-lug or the PCB-pin version.
- The slot's long axis runs **across** the row of pins (each blade's wide face toward its neighbour).
  - **Orientation confirmed by the user on the real switch (2026-10-09).**
- Board: SW1 updated in place, then re-routed with `_tools/autoroute.py --passes 400`: 25 vias; DRC 0 errors, 0 unconnected; parity clean.
  - The default 200 passes left R10 → C7 unrouted.
  - Backup before the change: `autoroute-backups/` (plus the pre-slot board in the session scratchpad).
- **Same footprint, still with round 1.3 mm holes:** Ugly Face 3 (THR), Rat Energizer (CLIP, OCT) and Harmonic Energizer (CLIP). Each has its own copy of `UglyFace.pretty`. Update them the same way at their next revisions. The **v1.1 boards just received have the small holes too.**
