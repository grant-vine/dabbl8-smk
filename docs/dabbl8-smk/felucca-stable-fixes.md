# Selective stable Felucca fixes for Dabbl8 SMK

Date: 2026-10-19. This is Phase 2 of the owner's authorized source maintenance,
after the [SMK 0.9.28 checkpoint](upstream-0.9.28.md). It does not begin the
eight-track composition port; that still depends on the main Dabbl8 project.

## Exact sources

- SMK source: `ChanceTheMaker/felucca-smk` at
  `4a6b332d3597fac6d2d9b053c50b3cad9eca0b77`.
- Phase 1 fork checkpoint: `af140032f1b9d3eaf107cf6de5ebb21544666a53`,
  [draft PR 1](https://github.com/grant-vine/dabbl8-smk/pull/1).
- Existing musical baseline: Felucca 1.5.1,
  `a4d7ca2e5d52a4c35e2468401f00d883cadbda03`.
- Selected stable reference: Felucca 1.6.1,
  `a53ecf428c29c780108fd70a31b71a32a6b5c313`, fetched read-only directly from
  `hugelton/Felucca`. The later main `5738617` was not imported.
- Implementation commit: `c9a6e1208d8480167d5b5bca1d8fd40251af1eb1` on
  `integrate/smk-felucca-1.6.1-fixes`, based on the Phase 1 branch.

This is a selective behavior port, not a merge or full upgrade to musical 1.6.1.
The generated firmware manifest correctly retains musical baseline 1.5.1.
Existing copyright and license notices are retained.

## Applicability decisions

| Stable fix / earlier relevant fix | Decision and SMK behavior |
| --- | --- |
| LARGE keeps one font per knob, 1.6.1 / #251 | **Applied to the active SMK renderer.** The SMK uses 116-pixel cards, so the initial envelope sweep did not reproduce FM-1's narrow-card size jumps. Its actual FUZZ card nevertheless chose the sparse L face without a Z glyph. `smk37_draw.c` now selects one supported face across the descriptor's entire formatted range, including units, and caches it per card/descriptor/font. LARGE values snap; normal-card rolling remains. The dormant FM-1 `ui_draw.c` is unchanged. |
| Bipolar percentages, 1.5.6 / #199 | **Applied.** Positive values use the 0..63 side's range; -64, 0 and 63 now show -100%, 0% and +100%. Both the actual SMK card and Device Studio's JS formatter are covered. Stored/raw values and sound are unchanged. |
| LED flash during save erase, 1.6 / #236 | **Applied with SMK hardware hooks.** Under the IRQ lock, the storage adapter blanks the existing SMK scanned-indicator commons before calling the RAM erase routine. The normal next scan resumes the indicators. No FM-1 LED GPIO operation is copied; latched RGB-pad behavior is unchanged. |
| Deferred LIST/FAV persistence, already in musical 1.5.1 / #197 | **Newly adapted to the SMK workflow.** The shared FM-1 implementation existed, but the SMK's own browser still queued writes on changing detents and redundant requests for unchanged values. Actual changes now coalesce until leaving the browser or ten seconds without panel input. Existing transport/held-note/storage gates still control the write. No-op detents do not dirty settings. |
| Browser session retention after that adaptation | **Preserved with a browser-only adjustment.** Virtual flash still processes pending favorites immediately, because browser snapshots copy that virtual flash before the hardware idle interval expires. An actual WASM panel-edit/snapshot/restore regression failed without this adjustment and passes with it. The browser session format is unchanged. |
| Automation row stability, 1.5.6 / #199 | **Already equivalent on SMK.** `smk37_graph_automation` walks physical record order; changing a parameter/value does not sort its row past another. The SMK has its own step/parameter/value controls, rather than FM-1's selected-row editor. The inactive FM-1 `motion_rows` parameter sort is not used by this view, so changing only that helper would not fix SMK behavior. No unnecessary sorting/UI port is included. |
| Wrong-board package refusal before erase, 1.6.1 | **Already enforced by the SMK implementation.** The SMKU header requires its own magic, exact 0x4000..0x9d000 interval and payload length, model/version, head/trim checks and checksums, followed by a complete payload preflight. Keep that pipeline and both-model wrapper gates. Do not copy FM-1's 0x93000 package size or staging/erase offsets. |
| BASS+ chord bounds/ownership | **Already present.** The shared chord implementation drops a seventh's fifth before inserting the lower root. The only SMK difference from the musical baseline is the board-sized key-owner arrays. No chord change exists between the selected 1.5.1 and 1.6.1 trees. Phase 1's chord/37-key ownership checks remain valid. |
| ARP follows held/latched TRN/ROOT/SCALE/QNT, 1.5 / #191; external-clock release fixes | **Already present.** Shared ARP logic and its regressions are retained, including the SMK's upper piano keys/pad ownership. No new ARP feature or duplicate fix is added. |
| USB audio interface collection ordering, 1.5.1 / #67 | **Already present.** `FELUCCA_UAC_AS_FIRST` and the matching collection layout remain in the shared USB implementation. Existing SMK SysEx, descriptor and MIDI-output adaptations are preserved. |
| MOMENTARY on FM-1 mixer, 1.5.1 / #195 | **Not applicable to this SMK control surface.** The shared FM-1 fix exists, but its held-LFO mixer interaction is not an SMK feature. Importing that control scheme would widen scope. |

The review also classified new conditional steps/FILL, EUCLID/DOUBLE/HALF,
SEQ+T, MIDI per-track routing/follow/wake, CLEAN INIT, project erase, new drum
kits, PHASE FOLD, modulation humanization, custom palettes, piano-roll auto-follow,
header redesign and inverted LED modes as **features excluded from this fix
round**. Second-core beta, its engine/voice/mixer/interrupt changes, and the
Felucca-Engines submodule/license restructuring are excluded too. Their new
formats, IDs and dependencies are not partially imported.

## Verification and observed failures

The owning regressions were extended before their fixes. Final checks passed:

| Check | Evidence |
| --- | --- |
| Visible SMK PAN endpoint and LARGE glyph/font behavior | `display-red-percent.log` failed +100; `display-red-glyph.log` failed FUZZ's missing Z; complete owner renderer suite passed in `display-final.log`. Full envelope ranges, engine endpoint/midpoint samples, both font weights, existing palettes/pages/styles/LCD bounds/IRQ checks and normal rolling remain covered. |
| Shipping JS percentage formatting and editor protocol suite | `editor-percent-red.log` had one failing endpoint; `editor-percent-green.log` ends `web tests passed`. Endpoint cases are outside optional external-fixture gates. |
| Real storage adapter sequencing against fakes | `save-led-red.log` reached erase without blanking; `save-led-green.log` passes. The test compiles the actual source function and checks IRQ-before-blank-before-erase, zeroed audio, rejected addresses/writability, returned error and IRQ restoration on success/failure. |
| Hardware browser-save scheduling | `browser-save-red.log` reproduced the immediate request. `workflow-preservation-green.log` passes changing/no-op detents, continued-input delay, ten-second boundary, view exit, single consumption and unsigned clock wrap, plus the existing workflow suite. |
| Browser virtual-save/session retention | `browser-save-snapshot-red-bank2.log` reproduced a lost filter after restore with the new delay. `browser-engine-snapshot-green.log` passes the actual panel navigation/edit/snapshot/restore plus the full existing engine/descriptor/sample/project/audio/release suite. |
| Audio worklet | `browser-worklet-snapshot.log`: 44.1/48 kHz audio, LCD/status, transport, release, snapshots and malformed-import rejection pass. |
| Live Panel and persistence preservation | Linux ASan programs `smk37_remote`, `smk37_workflow`, `smk37_test19`, `smk37_test23`; `workflow-preservation-green.log`. Earlier focused `smk37_upstream` and `smk37_store` checks are in `preservation-c.log`. |
| Final target | `target-build-final.log`: actual JieLi compile/link, application bounds, RAM-only flash routines and allocation checks pass. |
| Final application in Pro and Elite packages | `model-package-final.log`: both exact model wrappers/CRC/protected-byte roundtrips and malformed package rejection pass with the new application bytes. |
| Actual browser integration | `live-panel-browser-snapshot.log`: fresh headless Chrome, simulated MIDI, generated real C screen replies, input priority/FIFO, exact screen patches, old-firmware/reconnect gates, narrow screen assertion and rebuilt Browser Studio/Simulator switching pass. Worklet HTTP 200 is in `preview-server.log`. |

Native code runs used the existing network-disabled Linux amd64
`d8-clang18-selector:pinned` image, with
`clang-18 -D_POSIX_C_SOURCE=200809L -std=c99 -O1 -w -fsanitize=address`, generated
headers and the same includes as Phase 1. The C renderer and target use identical
font/table headers (hashes in the evidence manifest). The native save-order test
used `/usr/bin/python3` 3.9.6 and the host C compiler. Generation used the existing
isolated Python/Pillow environment from Phase 1. Browser compilation used pinned
Zig 0.13.0 installed only into ignored `build/wasm-tools/`; no global dependency
was changed. Its browser tests use the existing Playwright installation and
loopback server commands documented in Phase 1.

The first snapshot test attempted page navigation in knob bank 1, where that
encoder selects tracks. It correctly failed the page assertion
(`browser-save-snapshot-red.log`). Selecting navigation bank 2 made the test
reach the intended snapshot failure; no hardware-control mapping was changed.
The first LARGE sweep passed; its later FUZZ-specific assertion supplied the
actual missing-glyph failure. An early preview before initializing the palette
was black; the final owner test initializes palette/font, and the inspected
`stable-large-fuzz.png` shows the real C-rendered FUZZ card with intact letters.

Local editor diagnostics still parse included C fragments as standalone macOS
translation units, lacking generated includes and rejecting ELF sections. The
HTML editor also reports inherited accessibility diagnostics outside the changed
formatting expression. No clean whole-repository editor-lint result is claimed;
the actual target, Linux tests and executed browser checks above are the compile
and behavior evidence. No diagnostics or assertions were disabled for these fixes.

## Artifact identity and preservation

| Artifact | Identity |
| --- | --- |
| Final offline application | `build/phase2-target-final/smk37-integration-NOT-FOR-INSTALL.bin`, 421,320 bytes, SHA-256 `24627d59094b22a890ce476242ce2b5da4aeb8fc3f1ebc4dd5a320dfedbef72b` |
| Browser runtime | `web/audio/smk-engine.wasm`, 2,378,640 bytes, SHA-256 `8b5f1710a5c1312ea695a475902f09cf8a2827fdf77f876b14cfa198aad95e08` |
| Unchanged upstream published device application | 420,796 bytes, SHA-256 `b53614f3420d80bdc7ad31cf5b1d20ed35b4063fba4d64b70b1226c6bc498ab9` |

Relative to the Phase 1 local build, the final application grows by 524 bytes
and BSS by 128 bytes. `bss_end=0x1c18d5c`; `pool_end=0x1c73e58` is unchanged.
The RAM flash routines, data and noinit allocations are unchanged. The manifest
continues to say `installable: false`, with hardware validation false. No byte
reproducibility or device qualification is claimed.

A zero-diff comparison against Phase 1 covers the SMK flash allowlist, SMKU
format/core/loader, storage/sample/object/trim adapters, project/core formats,
controls/scanner, Live Panel protocol/input/screen sources, Windows helper and
installer paths, published application pins, licenses and credits. The only
hardware erase change is the tested sequencing around the existing guarded RAM
erase call. All existing protection predicates and ranges are retained.

All 12 original `.omo` planning/review files retain their Phase 1 hashes.
Phase 1 target output was restored to its original directory after the build
tool reused that directory; the final Phase 2 output has its own path above.
Durable local evidence is under
`/Users/grantv/Code/dabbl8-smk/.omo/evidence/felucca-stable-fixes-20261019/`.
The [machine-readable manifest](felucca-stable-fixes-evidence.json) records log,
source-preservation and artifact hashes. Generated device packages/stock fixtures
remain ignored and are not added to the PR. The generated browser runtime is
tracked with its existing non-executable permissions.

Unchanged Phase 1 helper/allowlist/restore tests were not repeated: their inputs
remain identical and their evidence is retained. Hardware installation/restore,
Elite/EB6014 qualification, Windows native locking/driver behavior and physical
timing remain untested locally. No MIDI device was opened or queried; no physical
flash/erase/write/reset/restore, merge, release or website deployment occurred.
The loopback preview server and temporary debug files were removed after checks.
