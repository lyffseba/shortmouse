# Stack

Reviewed: 2026-09-25.

This is the map from the tools this repository actually runs to the
official manuals for their latest stable releases. It covers four
things at the tip of the tree:

- the [`Makefile`](../Makefile)
- packaging: [`packaging/shortmouse.desktop`](../packaging/shortmouse.desktop) and the user-local install
- the shell scripts in [`scripts/`](../scripts)
- the CPython runtime the `shortmouse` package executes on

Pins use a numbered release, a frozen documentation snapshot, or the
manual shipped inside that release's tarball. Floating aliases
(`/latest/`, `docs.python.org/3/`, git `master`) are recorded only
where they have already drifted away from the numbered text.

GTK 4, libadwaita, AT-SPI, and PyGObject are the application libraries
named in the README install line. They are outside this pin set.

## Pins

| Area | Latest stable | Official docs pinned here | Release |
| --- | --- | --- | --- |
| Makefile | GNU Make 4.4.1 | [GNU Make Manual, edition 0.77](https://www.gnu.org/software/make/manual/make.html) (26 February 2023), for Make 4.4.1. The same text is `doc/make.texi` in the [4.4.1 tarball](https://ftp.gnu.org/gnu/make/make-4.4.1.tar.gz). | 26 February 2023 |
| Packaging | Desktop Entry Specification 1.5 | [Version 1.5](https://specifications.freedesktop.org/desktop-entry/1.5/) (published 2020-04-27). Keys: [recognized keys](https://specifications.freedesktop.org/desktop-entry/1.5/recognized-keys.html), [`Exec`](https://specifications.freedesktop.org/desktop-entry/1.5/exec-variables.html). | 27 April 2020 |
| Packaging | Desktop Menu Specification 1.1 | [Version 1.1](https://specifications.freedesktop.org/menu/1.1/) (20 August 2016). [`Utility`](https://specifications.freedesktop.org/menu/1.1/category-registry.html#main-category-registry) is a main category. Install locations: [locations](https://specifications.freedesktop.org/menu/1.1/locations.html). | 20 August 2016 |
| Packaging | Icon Naming Specification 0.8.90 | [Version 0.8.90](https://specifications.freedesktop.org/icon-naming/0.8.90/) (9 August 2007). `input-mouse` is a standard device icon. | 9 August 2007 |
| Packaging | XDG Base Directory Specification 0.8 | [Version 0.8](https://specifications.freedesktop.org/basedir/0.8/) (8 May 2021). | 8 May 2021 |
| Packaging | desktop-file-utils 0.28 | [Project page](https://www.freedesktop.org/wiki/Software/desktop-file-utils/). The tools check the Desktop Entry Specification; they have no separate user manual. Upstream NEWS date for 0.28 is 2024-10-25. | 25 October 2024 |
| Packaging | GNU coreutils 9.12 | [coreutils manual, edition 9.12](https://www.gnu.org/software/coreutils/manual/coreutils.html), last updated 12 September 2026, including [`install`](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html). Edition line is `doc/version.texi` in the [9.12 tarball](https://ftp.gnu.org/gnu/coreutils/coreutils-9.12.tar.xz). | 14 September 2026 |
| Scripts | Bash 5.3, patch 20 | [Bash Reference Manual, edition 5.3](https://www.gnu.org/software/bash/manual/bash.html), last updated 18 May 2025, for Bash 5.3. Sources: [bash-5.3.tar.gz](https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz) plus patches through [bash53-020](https://ftp.gnu.org/gnu/bash/bash-5.3-patches/bash53-020) (14 September 2026), which is Bash 5.3.20. | Manual 18 May 2025; patch 20 on 14 September 2026 |
| Language runtime | CPython 3.14.7 | [Python 3.14.7 documentation](https://docs.python.org/release/3.14.7/) (frozen snapshot). [Release](https://www.python.org/downloads/release/python-3147/) (5 August 2026). Schedule: [PEP 745](https://peps.python.org/pep-0745/). | 5 August 2026 |

CPython 3.15 is a pre-release (first release planned for 1 October 2026,
[PEP 790](https://peps.python.org/pep-0790/)). It is not a pin.

GNU Make development snapshots use a minor version of `.90` or higher
(4.4.90 is a pretest, not a release). None is newer than 4.4.1 on
`ftp.gnu.org/gnu/make/`.

## Drift on 2026-09-25

"Tree floor" is the oldest release that can run what the tip actually
uses. "Host" is the Ubuntu image this review was written on
(`python3` 3.12.3, Make 4.3, Bash 5.2.21, coreutils 9.4,
desktop-file-utils 0.27). A desktop's apt versions will differ.

| Tool | Tree floor | Pinned docs | Host that day | Drift |
| --- | --- | --- | --- | --- |
| GNU Make | `.PHONY` and `@echo`. Both are in Make 4.3 and 4.4.1. | 4.4.1, manual edition 0.77 | 4.3 | The manual matches the newest stable release. This host is one stable release behind. The Makefile does not use any 4.4 feature. |
| Bash | `BASH_SOURCE`, `[[ ]]`, `set -o pipefail`, here-strings. Present long before 5.2. | Manual edition 5.3 (18 May 2025). Sources are 5.3.20. | 5.2.21 | The official manual stopped at the 5.3 feature release. Twenty later official patches are bugfixes and do not have a newer manual edition. This host is still on the 5.2 series. |
| coreutils `install` | `install -m 0644` | 9.12, manual updated 12 September 2026 | 9.4 | The flag this script uses is unchanged across that span. The host manual is eight stable releases older than the pin. |
| desktop-file-utils | `desktop-file-validate`, `update-desktop-database` | 0.28 (2024-10-25) | 0.27 | `desktop-file-validate` 0.27 accepts `packaging/shortmouse.desktop` with no output. The 0.28 NEWS items (COSMIC, `Implements` groups) do not touch this file. |
| Desktop Entry spec | Keys listed below. `Version=` is omitted. | Numbered 1.5 | n/a | `/desktop-entry/latest/` still says version 1.5 and 2020-04-27, and its appendix B title differs ("Historically Reserved Items" there, "Currently reserved for use within KDE" in the numbered 1.5 text). The keys in this file are in both texts. |
| Menu spec | `Categories=Utility;` | 1.1 | n/a | `/menu/latest/` matches the numbered 1.1 text. |
| Icon naming spec | `Icon=input-mouse` | Numbered 0.8.90 | n/a | `/icon-naming/latest/` still says version 0.8.90 and adds a deprecated-names section plus later icon names. `input-mouse` is in the numbered 0.8.90 list. |
| XDG base directory | `~/.local/share` and `~/.local/bin` | Numbered 0.8 | n/a | `/basedir/latest/` still says version 0.8. It corrects typos and changes the directory-list separator from "a colon" to "the separator used for `$PATH`". The installer never reads those variables; it writes the 0.8 defaults. |
| CPython | 3.9, because [`shortmouse/hints.py`](../shortmouse/hints.py) evaluates `list[str]` ([PEP 585](https://peps.python.org/pep-0585/)) and does not import `annotations` from `__future__`. | 3.14.7 frozen docs | 3.12.3 | 3.9 is end-of-life (last release 3.9.25, 31 October 2025). 3.10 security support ends October 2026. 3.14 is the newest stable bugfix series. Unversioned `https://docs.python.org/3/` currently serves 3.14 and will move to 3.15 when that becomes stable. |

## Makefile

[`Makefile`](../Makefile) is a GNU Make file. Its targets are `help`,
`dump`, `run`, `install-user`, and `uninstall-user`. Every target is
listed in [`.PHONY`](https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html),
so Make runs the recipe even if a file with that name exists. `help`
prefixes its `echo` lines with `@`, which is Make's
[recipe echoing](https://www.gnu.org/software/make/manual/html_node/Echoing.html)
switch: the command is not printed, the text is.

`dump` and `run` set `PYTHONPATH=.` and run `python3 -m shortmouse`.
Make's recipe shell is `/bin/sh` (`SHELL`), not Bash. Those two
recipes stay within what `/bin/sh` can do. `install-user` and
`uninstall-user` hand off to the Bash scripts below.

The file uses no macros, pattern rules, automatic variables, or
includes. Reading order in the pinned manual: [rule syntax](https://www.gnu.org/software/make/manual/html_node/Rule-Syntax.html),
then Phony Targets, then Echoing.

## Packaging

There is no Python package metadata. No `pyproject.toml`, `setup.cfg`,
or `setup.py` is in the tree, so the [Python Packaging User Guide](https://packaging.python.org/)
does not describe this install. `.gitignore` mentions `.venv/`,
`*.egg-info/`, `dist/`, and `build/` anyway. Those names are unused.

What ships is a user install into the default XDG locations:

| Path the script writes | Spec |
| --- | --- |
| `$HOME/.local/share/shortmouse/` | [`$XDG_DATA_HOME`](https://specifications.freedesktop.org/basedir/0.8/), default `$HOME/.local/share`, plus an application directory under it |
| `$HOME/.local/share/applications/shortmouse.desktop` | [Menu spec install locations](https://specifications.freedesktop.org/menu/1.1/locations.html): `$XDG_DATA_HOME/applications` |
| `$HOME/.local/bin/shortmouse` | [Base directory spec](https://specifications.freedesktop.org/basedir/0.8/): user executables live in `$HOME/.local/bin`, which distributions put on `$PATH` |

`scripts/install-user.sh` assigns `PREFIX="${HOME}/.local"` and does
not read `$XDG_DATA_HOME`. A user who points that variable somewhere
else still gets files under `~/.local`. That matches the spec's
defaults and ignores an override.

### Desktop entry

[`packaging/shortmouse.desktop`](../packaging/shortmouse.desktop) is a
[Desktop Entry](https://specifications.freedesktop.org/desktop-entry/1.5/)
of `Type=Application`. The file name ends in `.desktop`. The install
script rewrites `Exec=` to the absolute path of `~/.local/bin/shortmouse`
before validation, which is the form the
[`Exec` key](https://specifications.freedesktop.org/desktop-entry/1.5/exec-variables.html)
expects when the binary is not being looked up on `$PATH` by the
installer itself.

| Key | Value | In spec 1.5 |
| --- | --- | --- |
| `Name` | shortmouse | Required |
| `GenericName` | Keyboard letter hints | Optional |
| `Comment` | Type letters to click GUI widgets… | Optional |
| `Exec` | `shortmouse` in git; absolute path after install | Required, because `DBusActivatable` is not set |
| `Icon` | `input-mouse` | Optional. An icon-theme name, defined in the [icon naming spec](https://specifications.freedesktop.org/icon-naming/0.8.90/) as the mousing device |
| `Type` | `Application` | Required |
| `Categories` | `Utility;` | Optional. The trailing semicolon is required. `Utility` is a [main category](https://specifications.freedesktop.org/menu/1.1/category-registry.html#main-category-registry) |
| `Terminal` | `false` | Optional boolean, valid because `Type=Application` |
| `StartupNotify` | `true` | Optional |
| `StartupWMClass` | `shortmouse` | Optional |
| `Keywords` | Shortcat;Hints;… | Optional. Also semicolon-separated |

The optional `Version` key is absent. Spec 1.5 says an entry that
conforms to that version should set `Version=1.5`, and also says the
field is not required. Adding it would be a packaging change; this
document only records the gap.

`install -m 0644` copies the desktop file. That is GNU
[`install`](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html)
from coreutils 9.12: copy a file and set its mode. `0644` is
owner-read/write, group-read, other-read.

When `desktop-file-validate` and `update-desktop-database` are on
`$PATH`, the install script runs them. Both come from
[desktop-file-utils](https://www.freedesktop.org/wiki/Software/desktop-file-utils/)
0.28. The validator's job is the Desktop Entry Specification, which is
why that spec is the pin and the utility has no manual of its own.
`update-desktop-database` rebuilds the MIME cache for the user
applications directory. The script passes `-q` and ignores a non-zero
status (`|| true`).

## Scripts

[`scripts/install-user.sh`](../scripts/install-user.sh) and
[`scripts/uninstall-user.sh`](../scripts/uninstall-user.sh) start with
`#!/usr/bin/env bash` and `set -euo pipefail`. They are Bash scripts.
The launcher they write to `~/.local/bin/shortmouse` is `#!/bin/sh`.

Pinned manual: [Bash Reference Manual, edition 5.3](https://www.gnu.org/software/bash/manual/bash.html)
(18 May 2025). The sections these scripts actually use:

| Script construct | Manual |
| --- | --- |
| `set -euo pipefail` | [The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html): `-e` exits on a failing command, `-u` errors on an unset parameter, `-o pipefail` makes a pipeline fail when any command in it fails |
| `${BASH_SOURCE[0]}` | [Bash Variables](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html). The install script resolves its own path, then the repo root |
| `[[ ... ]]` | [Conditional Constructs](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html) |
| `<<<"$existing"` | [Here Strings](https://www.gnu.org/software/bash/manual/html_node/Here-Strings.html), under Redirections |
| `${existing%]}` | [Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html): remove the shortest matching suffix |
| `command -v` | [Bourne Shell Builtins](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html). Used so missing optional tools are skipped |
| `cat >"$BIN" <<EOF` | [Here Documents](https://www.gnu.org/software/bash/manual/html_node/Here-Documents.html). The delimiter is unquoted, so the script escapes `$` where the generated file must contain a literal |

The generated launcher is POSIX `sh`, not Bash:

```sh
#!/bin/sh
export PYTHONPATH="${SHARE}${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m shortmouse "$@"
```

`python3 -m shortmouse` is the [CPython `-m` switch](https://docs.python.org/release/3.14.7/using/cmdline.html#cmdoption-m):
run the package's `__main__` module. See
[`__main__`](https://docs.python.org/release/3.14.7/library/__main__.html).

Two host commands are called when they exist, and their versions are
whatever GNOME the machine has. This repo does not pin a GLib or
gnome-settings-daemon release:

- `gsettings` reads and writes `org.gnome.settings-daemon.plugins.media-keys`, including the `custom-keybindings` array and the `shortmouse` custom-keybinding path. The binding it sets is `<Super><Shift>space`. Uninstall clears that entry's name, command, and binding and leaves the path in the array.
- `gio launch` is the command stored as the keybinding. It launches the installed desktop file.

`sed -i` in the install script is GNU sed's in-place edit. It is used
once, to replace the `Exec=` line. Sed is not otherwise part of this
stack.

## Language runtime

The runtime is CPython, invoked as `python3`. The package version in
[`shortmouse/__init__.py`](../shortmouse/__init__.py) is `0.1.0`.
There is no `python_requires` marker because there is no Python
package metadata.

Pinned documentation, frozen at the 3.14.7 release:

- [Documentation home](https://docs.python.org/release/3.14.7/)
- [Language reference](https://docs.python.org/release/3.14.7/reference/index.html)
- [What's new in 3.14](https://docs.python.org/release/3.14.7/whatsnew/3.14.html)
- [`dataclasses`](https://docs.python.org/release/3.14.7/library/dataclasses.html), used by `atspi_scan.py`

### Which Python the code can run

[`shortmouse/hints.py`](../shortmouse/hints.py) annotates with
`list[str]` and does not use `from __future__ import annotations`.
On 3.9 through 3.13 those annotations are evaluated when the function
is defined. `list[str]` works from 3.9 on
([PEP 585](https://peps.python.org/pep-0585/),
[what's new in 3.9](https://docs.python.org/release/3.14.7/whatsnew/3.9.html#pep-585-type-hinting-generics-in-standard-collections)).
That file sets the floor at 3.9. `dataclasses` is older than that.

The other modules do import annotations from `__future__`
([future statements](https://docs.python.org/release/3.14.7/reference/simple_stmts.html#future-statements),
[PEP 563](https://peps.python.org/pep-0563/)). Their annotations,
including `list[str] | None` in `__main__.py`, are stored as strings
and are not evaluated at definition time. That union syntax is why a
quick reading suggests a 3.10 floor. The import makes the expression
inert, so it does not raise the floor.

On 3.14 the default changed. [PEP 649 and PEP 749](https://docs.python.org/release/3.14.7/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations)
defer annotation evaluation, except in modules that still use
`from __future__ import annotations`. At the tip:

- `hints.py` follows the version default: eager on 3.9–3.13, deferred on 3.14 and newer.
- `__main__.py`, `overlay.py`, and `atspi_scan.py` keep PEP 563 string annotations on 3.14 as well.

3.14.7 is the newest stable release, in bugfix status until October
2030 ([PEP 745](https://peps.python.org/pep-0745/)). 3.13 is also in
bugfix. 3.12 and 3.11 are in security-only. 3.10's security window
ends October 2026. 3.9 is already end-of-life. Status is the table on
[python.org/downloads](https://www.python.org/downloads/).

## Re-pinning

Do this when an upstream stable release ships, or before a docs change
that touches these links. Skip alphas, betas, and release candidates.

1. CPython. Read [python.org/downloads](https://www.python.org/downloads/). Pin the newest series whose status is bugfix or security, and the newest patch of that series. Leave a pre-release series off the table. Point every Python link at `https://docs.python.org/release/X.Y.Z/`, which is frozen. `https://docs.python.org/3.14/` keeps moving inside the series. `https://docs.python.org/3/` jumps when a new series becomes the default. A patch of an older branch (a new 3.13.x while 3.14 is the pin) does not move the pin.
2. GNU Make. List `https://ftp.gnu.org/gnu/make/`. The pin is the highest version that is not a `.90`+ pretest. Open the manual's first page and confirm it still names that version. If the HTML on gnu.org has moved on, the previous pin is `doc/make.texi` inside the tarball you had recorded.
3. Bash. Take the newest `bash-X.Y.tar.gz` that is not labeled alpha, beta, or rc, then the highest `bashXY-NNN` file under `bash-X.Y-patches/`. Patch `NNN` means Bash `X.Y.NNN`. The reference manual is edition `X.Y`; it is not reissued for each patch. Record the manual date and the patch date separately.
4. coreutils. Take the newest `coreutils-X.Y.tar.xz` from `https://ftp.gnu.org/gnu/coreutils/`. The manual edition and its "last updated" date are `EDITION` and `UPDATED` in `doc/version.texi` inside that tarball. The gnu.org HTML is republished in place, so the tarball is the pin that cannot move under you.
5. Freedesktop specs. Open the numbered URL. If `/latest/` shows a higher version number, move the pin to that new number. If `/latest/` shows the same version and the words differ, keep the numbered URL and update the drift note. This review found that case for the desktop entry, icon naming, and base directory specs.
6. desktop-file-utils. Read the NEWS of the newest tarball under the [releases directory](https://www.freedesktop.org/software/desktop-file-utils/releases/). Re-run `desktop-file-validate packaging/shortmouse.desktop` when the pin moves.
7. Rewrite the host column from `make --version`, `bash --version`, `python3 --version`, `install --version`, and `desktop-file-validate --version`.
8. Change the "Reviewed" date at the top.

## Left out on purpose

The README's apt line installs `python3-gi`, `python3-gi-cairo`,
`gir1.2-gtk-4.0`, `gir1.2-adw-1`, and `gir1.2-atspi-2.0`. Those are the
GUI and accessibility libraries the program imports. They are not the
Make, packaging, script, or language-runtime tools, and this file does
not pin them.

`gsettings` and `gio` are host commands the Bash scripts call. Their
versions follow the installed GNOME. The script interface they use
(one media-keys schema, and `gio launch` of a desktop file) is
recorded above without a GLib version pin.
