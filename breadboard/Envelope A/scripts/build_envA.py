"""Ugly Face 1, envelope idea A (breadboard): drive the existing vactrol from a proper envelope follower.
  - Sidechain U1A (TL072): clean guitar from the UF1 IN pad (1M input, no extra loading), gain x3 to x49 (SENS),
    optional soft compression (R6 + D1/D2 across the feedback: quieter strings get relatively more envelope).
  - Tilt: C3 33n into R7 22k (~220 Hz high-pass) so the plain strings hit the detector about as hard as the low E.
  - Detector U1B: ideal-diode peak detector. Attack R8 1k x C4 1u (~1 ms), release R9 10k + DECAY B500k (10 ms to 0.5 s).
  - U2A (LM358): ENV straight into + (no load on the hold cap), R12 from +9V = 2 x VB, R13 fb: ENVD = 2 (ENV - VB),
    referenced to ground (LM358 output reaches 0 V). Ratiometric: VB is exactly +9V / 2 from the R1/R2 divider.
  - U2B (LM358) + Q1: current sink, I_LED = ENVD / R14 (330 ohm): ~0 to 18 mA. No LED threshold dead zone, so small
    envelopes still light the vactrol.
Connects to a UF1 v1.2 board: +9V, GND, IN tap; the vactrol LED leads move from U3 pads 1/2 to J4/J5 (LDR stays on the board).
usage: build_envA.py <out.kicad_sch>"""
from sch import *
import sys
OUT = sys.argv[1]
g = lambda n: round(n * 2.54, 3)
s = Sheet('EnvelopeA', 'A3')
W = lambda *p: s.wire(*p)
P = s.P
def GND(p): s.power('GND', p)
def VP(p): s.power('+9V', p)
def lab(n, p, side='r'): s.label(n, p, side)
def Rh(ref, v, cx, y, d='', text='t'): s.part(ref, 'Device', 'R', v, cx, y, 90, desc=d, text=text)
def Rv(ref, v, x, cy, side='r', d=''): s.part(ref, 'Device', 'R', v, x, cy, 0, desc=d, text=side)
def Ch(ref, v, cx, y, d='', text='t'): s.part(ref, 'Device', 'C', v, cx, y, 90, desc=d, text=text)
def Cv(ref, v, x, cy, side='r', d='', pol=False): s.part(ref, 'Device', 'C_Polarized' if pol else 'C', v, x, cy, 0, desc=d, text=side)
def pad(ref, name, x, y, rot=180, text='t'): s.part(ref, 'Connector_Generic', 'Conn_01x01', name, x, y, rot, desc=name, text=text)
PINS = {1: ('3', '2', '1'), 2: ('5', '6', '7')}
def OP(ref, lib, unit, x, ytop):
    s.part(ref, 'Amplifier_Operational', lib, lib, x, ytop + 2.54, 0, unit=unit, text='ic')
    pl, mi, ou = PINS[unit]
    return P(ref, pl), P(ref, mi), P(ref, ou)
def to_lab(p, name, dx, side='r'):
    q = (p[0] + dx, p[1]); W(p, q); lab(name, q, side)
def to_vb(p):  # short drop to a VB label below a vertical part's bottom pin
    q = (p[0], p[1] + g(1)); W(p, q); lab('VB', q, 'l')

# ================================================================ CONNECTIONS + POWER
s.box('CONNECTIONS (to a UF1 v1.2 board) + POWER', g(2), g(2), g(34), g(44))
pad('J1', '+9V (UF1 C1+)', g(6), g(8)); W(P('J1', '1'), (g(14), g(8))); VP((g(14), g(8))); s.power('PWR_FLAG', (g(14), g(8)))
pad('J2', 'GND (UF1 J2)', g(6), g(13)); W(P('J2', '1'), (g(14), g(13))); GND((g(14), g(13))); s.power('PWR_FLAG', (g(12), g(13)))
pad('J3', 'IN tap (UF1 IN)', g(6), g(18)); to_lab(P('J3', '1'), 'IN', g(4))
Rv('R1', '10k', g(22), g(10), d='VB divider'); VP(P('R1', '1'))
Rv('R2', '10k', g(22), P('R1', '2')[1] + g(2) + 3.81, d='VB divider'); GND(P('R2', '2'))
vb = (g(22), P('R1', '2')[1] + g(1)); W(P('R1', '2'), vb, P('R2', '1'))
Cv('C5', '47u', g(27), vb[1] + 3.81, d='VB filter', pol=True); W(vb, (g(27), vb[1]), P('C5', '1')); GND(P('C5', '2'))
W((g(27), vb[1]), (g(31), vb[1])); lab('VB', (g(31), vb[1]))
s.part('U1', 'Amplifier_Operational', 'TL072', 'TL072', g(10), g(34), 0, unit=3, text='ic'); VP(P('U1', '8')); GND(P('U1', '4'))
s.part('U2', 'Amplifier_Operational', 'LM358', 'LM358', g(18), g(34), 0, unit=3, text='ic'); VP(P('U2', '8')); GND(P('U2', '4'))
Cv('C6', '100n', g(25), g(34), d='U1 decoupling'); VP(P('C6', '1')); GND(P('C6', '2'))
Cv('C7', '100n', g(30), g(34), d='U2 decoupling'); VP(P('C7', '1')); GND(P('C7', '2'))

# ================================================================ SIDECHAIN (U1A) + TILT
s.box('SIDECHAIN U1A: clean guitar x3 to x49 (SENS), optional soft compression; TILT high-pass ~220 Hz', g(38), g(2), g(100), g(44))
pl, mi, ou = OP('U1', 'TL072', 1, g(62), g(10))
lab('IN', (g(41), pl[1]), 'l'); W((g(41), pl[1]), (g(43), pl[1]))
Ch('C1', '100n', g(43) + 3.81, pl[1], d='Input coupling'); nin = (g(50), pl[1]); W(P('C1', '2'), nin, pl)
Rv('R3', '1M', nin[0], nin[1] + g(1) + 3.81, d='Bias to VB (1M: no extra load on the guitar)'); W(nin, P('R3', '1')); to_vb(P('R3', '2'))
NX = mi[0] - g(1); rx = ou[0] + g(2)
W(mi, (NX, mi[1]))
gl = (g(54), mi[1]); W((NX, mi[1]), gl)
Rv('R5', '2k2', gl[0], gl[1] + g(1) + 3.81, side='l', d='Gain leg'); W(gl, P('R5', '1'))
Cv('C2', '22u', gl[0], P('R5', '2')[1] + g(1) + 3.81, side='l', d='Gain-leg DC block (DC gain 1)', pol=True); W(P('R5', '2'), P('C2', '1')); to_vb(P('C2', '2'))
f1, f2, f3, f4 = (mi[1] + g(k) for k in (4, 7, 10, 12))
W((NX, mi[1]), (NX, f3))
Rh('R4', '4k7', NX + g(1) + 3.81, f1, d='Minimum gain'); W((NX, f1), P('R4', '1'))
pc = P('R4', '2')[0] + g(1) + 3.81
s.part('RV1', 'Device', 'R_Potentiometer', 'B100k', pc, f1, 90, desc='SENS (sidechain gain)', extra={'Panel': 'SENS'},
       text=((pc + g(3), f1 + g(1.2)), (pc + g(3), f1 + g(2.4)), 'left'))
W(P('R4', '2'), P('RV1', '1')); w = P('RV1', '2'); p3 = P('RV1', '3'); W(w, (p3[0], w[1]), p3)
rx = max(rx, p3[0] + g(1))
W(p3, (rx, f1))
Ch('C8', '100p', NX + g(1) + 3.81, f2, d='HF limit', text='t'); W((NX, f2), P('C8', '1')); W(P('C8', '2'), (rx, f2))
Rh('R6', '10k', NX + g(1) + 3.81, f3, d='COMP option: soft compression (fit R6 + D1/D2, or leave all out)')
W((NX, f3), P('R6', '1')); xc = P('R6', '2')[0] + g(1); W(P('R6', '2'), (xc, f3))
s.part('D1', 'Device', 'D', '1N4148', xc + g(1) + 3.81, f3, 180, desc='COMP option', text='t'); W((xc, f3), P('D1', '2')); W(P('D1', '1'), (rx, f3))
s.part('D2', 'Device', 'D', '1N4148', xc + g(1) + 3.81, f4, 0, desc='COMP option', text='b'); W((xc, f3), (xc, f4), P('D2', '1')); W(P('D2', '2'), (rx, f4))
W(ou, (rx, ou[1])); W((rx, ou[1]), (rx, f4))
# tilt
Ch('C3', '33n', rx + g(2) + 3.81, ou[1], d='TILT: with R7 ~220 Hz high-pass (try 47n = 150 Hz, 22n = 330 Hz)'); W((rx, ou[1]), P('C3', '1'))
tn = (P('C3', '2')[0] + g(2), ou[1]); W(P('C3', '2'), tn)
Rv('R7', '22k', tn[0], tn[1] + g(1) + 3.81, d='TILT'); W(tn, P('R7', '1')); to_vb(P('R7', '2'))
to_lab(tn, 'SC', g(3))

# ================================================================ DETECTOR (U1B)
s.box('DETECTOR U1B: peak detector, attack ~1 ms, DECAY 10-500 ms', g(104), g(2), g(152), g(44))
pl, mi, ou = OP('U1', 'TL072', 2, g(118), g(10))
lab('SC', (g(108), pl[1]), 'l'); W((g(108), pl[1]), pl)
s.part('D3', 'Device', 'D', '1N4148', ou[0] + g(1) + 3.81, ou[1], 180, desc='Ideal-diode rectifier', text='t'); W(ou, P('D3', '2'))
Rh('R8', '1k', P('D3', '1')[0] + g(1) + 3.81, ou[1], d='ATTACK (with C4: ~1 ms)'); W(P('D3', '1'), P('R8', '1'))
env = (P('R8', '2')[0] + g(2), ou[1]); W(P('R8', '2'), env)
Cv('C4', '1u', env[0], env[1] + g(1) + 3.81, d='Hold cap (film or X7R)'); W(env, P('C4', '1')); GND(P('C4', '2'))
ex = env[0] + g(5)
W(env, (ex, env[1]))
Rv('R9', '10k', ex, env[1] + g(1) + 3.81, d='Minimum release'); W((ex, env[1]), P('R9', '1'))
s.part('RV2', 'Device', 'R_Potentiometer', 'B500k', ex, P('R9', '2')[1] + g(1) + 3.81, 0, desc='DECAY (release to VB)', extra={'Panel': 'DECAY'}, text='r')
W(P('R9', '2'), P('RV2', '1')); w = P('RV2', '2'); p3 = P('RV2', '3'); W(w, (w[0], p3[1]), p3); to_vb(p3)
# feedback from ENV to U1B - (closes the ideal-diode loop)
fb = mi[1] + g(6)
W(env, (env[0], env[1] - g(4)))
W(mi, (mi[0] - g(2), mi[1]), (mi[0] - g(2), env[1] - g(4)), (env[0], env[1] - g(4)))
to_lab((ex, env[1]), 'ENV', g(3))

# ================================================================ ENV - VB (U2A)
s.box('U2A (LM358): ENVD = 2 x (ENV - VB), referenced to GND; ENV unloaded', g(2), g(50), g(70), g(92))
pl, mi, ou = OP('U2', 'LM358', 1, g(40), g(64))
lab('ENV', (pl[0] - g(6), pl[1]), 'l'); W((pl[0] - g(6), pl[1]), pl)   # straight into + : no load on the hold cap
md = (mi[0] - g(1), mi[1])
Rh('R12', '10k', mi[0] - g(2) - 3.81, mi[1] + g(6), d='Offset: from +9V (= 2 x VB, ratiometric)'); W(mi, md, (md[0], mi[1] + g(6)), P('R12', '2'))
q = P('R12', '1'); W(q, (q[0] - g(2), q[1])); VP((q[0] - g(2), q[1]))
rxa = ou[0] + g(2)
Rh('R13', '10k', (md[0] + rxa) / 2, mi[1] + g(9), d='Feedback'); W((md[0], mi[1] + g(6)), (md[0], mi[1] + g(9)), P('R13', '1'))
W(P('R13', '2'), (rxa, mi[1] + g(9)), (rxa, ou[1]), ou)
to_lab((rxa, ou[1]), 'ENVD', g(3))

# ================================================================ LED DRIVER (U2B + Q1)
s.box('DRIVER U2B + Q1: current sink, I_LED = ENVD / 330 (0-18 mA)', g(74), g(50), g(152), g(92))
pl, mi, ou = OP('U2', 'LM358', 2, g(96), g(72))
lab('ENVD', (g(84), pl[1]), 'l'); W((g(84), pl[1]), pl)
Rh('R16', '1k', ou[0] + g(1) + 3.81, ou[1], d='Base resistor'); W(ou, P('R16', '1'))
qx = P('R16', '2')[0] + g(1) + 5.08
s.part('Q1', 'Device', 'Q_NPN', '2N3904', qx, ou[1], 0, desc='LED current sink', text='r'); W(P('R16', '2'), P('Q1', 'B'))
e = P('Q1', 'E'); c = P('Q1', 'C')
Rv('R14', '330', e[0], e[1] + g(1) + 3.81, d='Sets I_LED = ENVD / 330: ~0-18 mA'); W(e, P('R14', '1')); GND(P('R14', '2'))
en = (e[0], e[1] + g(1))
W(mi, (mi[0] - g(2), mi[1]), (mi[0] - g(2), en[1] + g(6)), (e[0] - g(3), en[1] + g(6)))
W((e[0] - g(3), en[1] + g(6)), (e[0] - g(3), en[1]), en)
pad('J5', 'Vactrol LED cathode', c[0] + g(6) + 5.08, c[1] - g(2), 0, text='r'); W(c, (c[0], c[1] - g(2)), P('J5', '1'))
pad('J4', 'Vactrol LED anode', c[0] + g(6) + 5.08, c[1] - g(9), 0, text='r')
Rv('R15', '100', c[0], c[1] - g(9) - g(1) - 3.81, d='LED supply: limits Q1 dissipation'); VP(P('R15', '1'))
W(P('R15', '2'), (c[0], c[1] - g(9)), P('J4', '1'))

notes = ('Hook-up to a UF1 v1.2 board:',
         '1. +9V from C1 + (or the D1 cathode), GND from J2, IN tapped from the IN pad (J3 pin 1).',
         '2. Unsolder the vactrol LED leads from U3 pads 1/2 and run them to J4 (anode) / J5 (cathode). Leave the LDR on pads 3/4.',
         '3. ENV on the board then does nothing (its wiper is open). Use SENS here instead.',
         'Start: SENS mid, DECAY mid, COMP parts out, TILT 33n. Compare low E vs high E, then try COMP and TILT 47n / 22n.')
for i, t in enumerate(notes): s.text(t, g(4), g(98 + 2.5 * i), 1.5)
s.write(OUT, shift=(g(4), g(4)), title_block={'title': 'Ugly Face 1: envelope idea A (breadboard)', 'rev': '0.1', 'company': 'Super-Freq',
                         'comments': ['Clean sidechain + tilt + peak detector + current-sink vactrol driver', 'Breadboard add-on for a UF1 v1.2 board']})
