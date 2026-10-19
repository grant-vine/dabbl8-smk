# Dabbl8 SMK repository instructions

Model routing: use GPT-6.1 Sol with xhigh reasoning for substantive work and
GPT-6 Luna for routine/background tasks. Do not select Astra without the owner's
explicit request. Preserve this policy during tooling upgrades.

Read [docs/UPSTREAM_WORKFLOW.md](docs/UPSTREAM_WORKFLOW.md) before importing
upstream changes, preparing contributions, changing firmware protocols, or
publishing a release. These are Salt's operating rules, not upstream policy.

- Our writable repository is `grant-vine/dabbl8-smk`. Treat
  `ChanceTheMaker/felucca-smk` (SMK source upstream) and `hugelton/Felucca`
  (musical upstream) as read-only destinations. Here `origin` is the Dabbl8 SMK
  fork and `upstream` is ChanceTheMaker's SMK repository. Legacy examples in
  `docs/UPSTREAM_WORKFLOW.md` describe the original Salt fork; do not copy their
  push destinations. Inspect remote URLs and use an explicit owned-fork URL.
- Shared Dabbl8 composition/project architecture remains governed by the main
  Dabbl8-first plan. Separately authorized SMK source maintenance is allowed;
  it does not begin the wider eight-track device port. See
  `docs/dabbl8-smk/upstream-0.9.28.md` and
  `docs/dabbl8-smk/felucca-stable-fixes.md` for the maintenance checkpoints.
- Fetch, compare, test, and prepare focused changes autonomously within the
  current task. Keep unrelated features in separate branches and PRs.
- Never submit the Salt branch wholesale upstream. Prepare each proposed
  contribution from current upstream main and include only that feature.
  Sending an upstream PR or message requires the owner's authorization for
  that contribution; this does not block local preparation or authorized fork PRs.
- Preserve upstream command IDs, storage migrations, author credits and licenses.
  Negotiate new protocol extensions; do not commandeer an existing command.
- Keep experimental Bluetooth work excluded unless the owner explicitly changes
  its scope. Do not copy build outputs or firmware from that worktree.
- Keep website publication separate from firmware release. A host-tested
  candidate does not replace the published firmware before hardware validation.
- Record the upstream revision, retained Salt differences, test evidence,
  skipped checks, and contribution status in the tracking documents. When
  upstream adopts a feature, reconcile our implementation and retire duplication.

The owner's explicit instructions in the current session take precedence.

Deferred requests are recorded in [docs/WORK_QUEUE.md](docs/WORK_QUEUE.md).
Do not silently include queued features in an unrelated active round.
