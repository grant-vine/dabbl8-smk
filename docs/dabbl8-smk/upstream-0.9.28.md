# Dabbl8 SMK 0.9.28 source checkpoint

Date: 2026-10-19. Repository: `grant-vine/dabbl8-smk`.

Phase 1 imports the pinned SMK maintenance release and verifies it locally.
It does not start the Dabbl8 composition port. The main Dabbl8 project must
finish the shared architecture first; its approved planning remains the
dependency for that later port. Phase 2 needs a separate go-ahead.

## Source and retained differences

- Previous fork main: `00197c1761d060546d07e658c17088477e472482`
  (Felucca SMK 0.9.24).
- SMK source upstream: `ChanceTheMaker/felucca-smk`, pinned at
  `4a6b332d3597fac6d2d9b053c50b3cad9eca0b77` (0.9.28 beta).
- Musical upstream remains Felucca 1.5.1,
  `a4d7ca2e5d52a4c35e2468401f00d883cadbda03`. Felucca 1.6.1 and the
  coordinator's shared-fix phase are excluded from this checkpoint.
- Integration branch: `integrate/smk-0.9.28`, worktree
  `/private/tmp/dabbl8-smk-0928-20261019`. It fast-forwards the old main to
  the pinned SMK revision, preserving all six incoming commits and authors.
  The primary checkout's `main` is not advanced by preparing this branch.

| Incoming commit | Scope |
| --- | --- |
| `d52e437c592e79a76f1bf04d34a40779c57db794` | 0.9.27 Live Panel, screen deltas and physical-control protocol |
| `ba2e583f37fa79e937ae4f4f6dd4e6ded4d300ea` | Homepage and connected-device wording |
| `1e4bb38c18d06f77757029f1ba4876bfc0856cf6` | Windows Pro native installer and restore helper |
| `1760f23a78ad59a0ce1c8a58a4b0c4c3a50db731` | Exact flash IDs and explicit loader/restore failure diagnostics |
| `0b760a21ab9d978eaa5138f3a1a11db23fc654eb` | Upstream 0.9.28 application and matching public installer pins |
| `4a6b332d3597fac6d2d9b053c50b3cad9eca0b77` | Matching build and helper documentation |

The fork had no tracked runtime divergence to reapply. Its existing 12
untracked `.omo` planning/review files were preserved byte for byte, including
the approved main-first plan (SHA-256
`f23907b9df0b34924d82a3803554407185e225e3e08454938da9b6cf59024a66`).
Their historical 0.9.24 baseline is intentionally retained; this document
records the separately authorized maintenance update.

The local additions are this checkpoint/evidence record, corrected fork
ownership/model instructions in `AGENTS.md`, a status entry, and a repair to
the editor regression's incomplete simulated-device replies. Firmware and
shipping web code remain identical to the pinned SMK source.

The project, preset, sample/object storage adapters, trim adapter, project
source, `LICENSE` and `LICENSING.md` have no diff between the two SMK revisions.
Existing protocol IDs and credits are preserved. The flash allowlist is exactly
`0x856014` and `0xEB6014`; unrelated same-density IDs remain rejected. App-only
updates retain the protected application interval `[0x4000, 0x9D000)`.
The new checksummed `0x7E` loader diagnostic uses the existing OTA envelope and
a 12-byte `SMKU` version-1 body; it reports the error, attempted-write flag and
observed JEDEC ID. See [upstream compatibility details](../smk37/FLASH_COMPATIBILITY.md).

Windows native routing applies to Pro only. Elite retains the browser route.
An old rejecting loader cannot acquire this fix merely by being given the new
application package; the separate recovery limits still apply.

## Local verification

All final checks below passed. Device transports use fakes/fixtures; no physical
device was opened, queried, reset, restored or flashed.

| Check | Observed result / evidence log |
| --- | --- |
| `sh tools/test_smk37_public.sh` | ASan/UBSan updater rejection, corruption, interruption/retry, protected bounds and exact flash allowlist; `updater-sanitizers.log` |
| `sh tools/test_smk37_controls.sh` | Controls/HAL/startup suite; `controls.log` |
| Linux application suite | 22 C test programs including Live Panel screen/input, storage, MIDI and migration under ASan; `linux-application-asan-posix.log` |
| `python3 -m unittest discover -s tests -p 'smk37_*_test.py'` | 71 tests; `python-smk-suite.log` |
| `python3 tests/native_smk.py` | 8 fake-wire transport tests; `native-transport.log` |
| `python3 tests/smk_diagnostics.py` and `node tests/smk_diagnostics.mjs` | 4 Python tests and shipping JS diagnostic parsing; `diagnostics-python.log`, `diagnostics-js.log` |
| `node tests/native_smk_client.mjs` | Helper version/token/absence/denial and platform/model isolation; `native-client.log` |
| `python3 tests/native_smk_http.py` | Loopback Host/Origin/token/fixed-action boundaries, no device job; `native-http-retry.log` |
| `node tests/native_smk_ui.mjs` | Simulated Windows Pro install/restore, no browser-MIDI fallback on helper failure, document/port cleanup; `native-browser.log` |
| Shipping wire integration | 1,619 actual C replies plus completion/menu/preferences/sample fixtures parsed by shipping JS; `shipping-{wire,completion,menu,preferences,samples}.log` |
| `node web/test_smk_remote.mjs` | Actual C screen fixtures, exact pixels, input order/priority, screen polling, simulated 50 ms USB, browser reconnect, old-firmware gate, Browser Studio/Simulator switching and narrow-screen assertion; `live-panel-browser-served.log` |
| `node web/test_smk37_browser.mjs` | Actual descriptors, 37 keys, INSERT cards, MIDI learn, nudge, eight user slots, four song lanes; `descriptor-browser-fixed.log` |
| Web/helper regression group | 14 JS scripts listed below; their individual logs |
| `node web/restore-stock/test_restore.mjs` with both pinned stock fixtures | Both model containers, corruption/wrong-model rejection, interruption/no retry and exact return identity; `stock-restore.log` |
| `tools/build_smk37.py --public-release --panel-mirror --usb-test-number 28` | Target links, protected bounds and RAM-only flash routines checked; `target-build.log` |
| `node web/test_smk37_public.mjs <pro> <elite> <local-manifest>` | Both model wrapper/CRC/protected-byte and malformed-application checks; `model-package-roundtrip.log` |
| `node tools/native_smk_package.mjs install public build/phase1-native-package` | Local Pro helper packaging verifies the unchanged published upstream application; `native-package.log`, generated `verified.json` |
| `python3 tools/make_smk_site.py build/phase1-site` | Local staging only; `site-staging.log` |

The 14 JS scripts are `web/test_update_progress.mjs`, `web/test_midi_input.mjs`,
`web/audio/test_smk_engine.mjs`, `web/audio/test_smk_worklet.mjs`,
`web/test_midi_diagnostics.mjs`, `web/test_smk37_handoff.mjs`,
`web/test_smk37_update.mjs`, `web/test_install_flow.mjs`,
`web/test_discovery.mjs`, `web/test_panel_glide.mjs`, `web/test_locales.mjs`,
`web/test_analytics.mjs`, `web/test_web.mjs`, and `web/test_keyboard_glide.mjs`.
Translations cover all eight languages and 505 matching keys/placeholders.

### Environment and corrected harness failures

- Host: macOS ARM64, Apple clang 21, Node 26.12.0, default Python 3.15.0.
  Header generation/target builds used the existing Dabbl8 isolated Python
  3.14.8 environment with Pillow 12.3.0 and raqm enabled.
- Target compiler: existing `jieli-linux-toolchains-20250324.1`, through
  `debian:bookworm-slim` image ID
  `sha256:d4c45f66efc59f89b0597d343a9bd72808493c0eacecde5285961743252cee23`.
- Native macOS application tests cannot compile the firmware's ELF `.pool`
  sections as Mach-O (`application.log`). The C suite instead used Linux amd64
  image `d8-clang18-selector:pinned`, ID
  `sha256:32e3e3e3a5751a9cffb34f767502920c932e77e9af24878dba5d9adc840ec71a`,
  `clang-18 -D_POSIX_C_SOURCE=200809L -std=c99 -O1 -w -fsanitize=address`
  and the generated headers from the successful target build. Docker networking
  was disabled. The initial strict-C99 attempt lacked POSIX clock declarations
  (`linux-application-asan.log`); the harness macro corrected that build setup.
  The shipping JS checks ran separately on the host because this Linux image
  has no Node or Pillow. No test assertions were suppressed.
- The first shipping wire invocation omitted its required fixture argument
  (`test_smk37_wire.mjs.log`). The successful invocation is
  `node web/test_smk37_wire.mjs build/smk37-tests/editor-wire.jsonl`.
- The initial HTTP test was blocked by sandbox loopback-bind permissions
  (`native-http.log`). It passed with the permitted loopback server scope.
- The first Live Panel browser run had no listener on port 8820. Its page-route
  fixture served the editor, but the AudioWorklet request failed with a network
  error (`live-panel-browser.log`). The unchanged test passed after starting
  `python3 -u tools/serve_smk37.py --port 8820`. The server recorded HTTP 200
  for the worklet (`preview-server.log`). No product reconnect fix was required.
- The adjacent editor test advertised preference/menu capabilities but omitted
  the corresponding fake replies. It timed out after command 34
  (`descriptor-browser.log`). Adding real C workflow/menu fixtures, matching
  menu replies by ID and echoing variable favorites queries fixed the harness
  (`descriptor-browser-fixed.log`). Every pre-existing assertion is retained;
  `web/test_smk37_preferences.mjs` and `web/test_smk37_menu.mjs` also validate
  the actual firmware replies independently.
- Browser tests used installed headless Chrome with fresh profiles and
  `PLAYWRIGHT_MODULE=/Users/grantv/Code/dabbl/website/node_modules/playwright/index.mjs`.
  For the descriptor test, `SITE_URL=http://127.0.0.1:8820`; Live Panel uses
  its default `http://localhost:8820`. The preview server is stopped after checks.
- `python3 tests/native_smk_lock.py` explicitly skipped its Windows-only file
  locking test on macOS (`windows-lock.log`). A real Windows helper installation,
  Windows MIDI stack and Windows process-lock behavior remain unverified here.

## Build and fixture identity

The rebuilt application is 420,796 bytes, product `SMK-37_928`, Live Panel
protocol 4. Its generated manifest explicitly says `installable: false` and
marks device validation false.

| Application | SHA-256 |
| --- | --- |
| Local `build/smk37-panel-mirror-candidate/smk37-integration-NOT-FOR-INSTALL.bin` | `f09af2250dc4566ee301840a463d28e2f56b9504421e2f0973cd07173d952171` |
| Unchanged upstream `web/firmware/felucca-smk-0.9.28-app.bin` | `b53614f3420d80bdc7ad31cf5b1d20ed35b4063fba4d64b70b1226c6bc498ab9` |

The byte hashes differ despite the equal size. Byte reproducibility is not
established; the cause has not been proven. The local application was used only
for offline package tests. It did not replace the published upstream component
or any installer pin. The helper-package check separately used that pinned
upstream component.

Both official 016 stock containers came from the existing public mirror at
`jonathaslacerda/smk-37-pro-docs` revision
`ab85d7340163ba9e171dc9396e31c034829bbc02`, paths
`firmware/smk37pro/SMK-37_Pro_016.fwsc` and
`firmware/smk37elite/SMK-37_Elite_016.fwsc`.

- Pro SHA-256: `2d98ce72530e71d617384963423820536f094501299e2cfec0a8d3c3fb6bcfb0`.
- Elite SHA-256: `b2ee38abfef3ae922e4eecdb8a551e14345300ae6f270265feacd33b6ef99cb6`.

These fixtures and locally generated packages stay in ignored `build/` paths;
they are not newly committed or installed.

## Evidence and phase boundary

Local logs are in the integration worktree's `build/phase1-evidence/`, with a
durable copy under the primary checkout at
`.omo/evidence/upstream-0.9.28-20261019/`. Log hashes, artifact identities and the
preserved planning hashes are recorded in [the evidence manifest](upstream-0.9.28-evidence.json).
Browser screenshots are `build/panel-preview/device-mirror-fixture.png`,
`build/panel-preview/device-screen-only.png`, and
`build/screenshots/smk37-upstream-sequencer.png`; local copies accompany the logs.

Upstream's prior 856014 Pro round-trip record is upstream evidence, not a test
of this owner's Elite or the local rebuild. Elite and EB6014 physical validation,
real USB timing/audio, hardware installation/restore and Windows locking are
outside this local checkpoint. No release or website was published, no firmware
was promoted, and no device operation occurred. The inherited Pages workflow
also guards publication to `ChanceTheMaker/felucca-smk` only.

This branch is a source review checkpoint. Stop after recording it; await the
coordinator's explicit Phase 2 go-ahead before importing shared Felucca fixes.
