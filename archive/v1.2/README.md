# Ugly Face 1 SMD v1.2: archived revision

- **Git tag:** `v1.2` (commit `d936919`, 2026-10-06)
- **Tag note:** v1.2: ordered from JLCPCB (October 2026 batch)
- **Archived:** 2026-10-06 with `_tools/archive_version.py`

## Finding a part

1. Open `UglyFace_01_ibom.html` in a browser. Type a reference (R14) or a value (100k) in the filter box; the part lights up on the board.
   - Hover over a pad to see its net.
   - F / B switch sides.
2. Find the same reference in `UglyFace_01_schematic.pdf` with Cmd-F.
3. `UglyFace_01_board_front.pdf` / `_back.pdf` are printable: page 1 has the outlines and references, page 2 the copper. The back is mirrored, as you see it holding the board.

## Files

- `UglyFace_01_board_back.pdf`
- `UglyFace_01_board_front.pdf`
- `UglyFace_01_ibom.html`
- `UglyFace_01_render_bottom.png`
- `UglyFace_01_render_top.png`
- `UglyFace_01_schematic.pdf`
- `docs`/
- `parts.csv`
- `production`/

`production/` holds the files sent to JLCPCB for this revision: UglyFace_01.zip, bom.csv, designators.csv, netlist.ipc, positions.csv.

## Added 2026-10-09 (while building the v1.2 boards)

- `kicad/`: the v1.2 KiCad project files exactly as tagged (schematic, board, footprints), so the as-built design can be opened even after the working copy moves on.
- `build-docs/`: documents written while building and testing v1.2: `Test Sheet v1.2.md` (bench results), `Debug - Unit 1 hot 555.md` (v1.0 latch-up analysis, retrofit), `Build Notes.md` (incl. the toggle-hole and LDR notes).
- **Changes after v1.2 in the working copy (not on these boards):** SW1 footprint → plated slots 2.6 × 1.1 mm (Taiway pins/lugs didn't fit the 1.3 mm holes) and a re-route.
