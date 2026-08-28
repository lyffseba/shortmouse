"""CLI: `python3 -m shortmouse` or `shortmouse`."""

from __future__ import annotations

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio  # noqa: E402

from shortmouse.atspi_scan import scan
from shortmouse.hints import make_labels
from shortmouse.overlay import OverlayWindow

APP_ID = "dev.lyffseba.Shortmouse"


def dump() -> int:
    targets = scan()
    labels = make_labels(len(targets))
    print(f"targets={len(targets)}")
    for label, t in zip(labels, targets):
        print(
            f"{label:4}  {t.title[:40]!r:42}  {t.role:16}  "
            f"{t.app}  @ {t.x},{t.y} {t.w}x{t.h}"
        )
    return 0


class Shortmouse(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.NON_UNIQUE)

    def do_activate(self) -> None:  # noqa: N802
        targets = scan()
        labels = make_labels(len(targets))
        for label, target in zip(labels, targets):
            target.label = label
        win = OverlayWindow(self, targets, on_done=self.quit)
        win.present()


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv if argv is None else argv)
    if "--dump" in argv:
        return dump()
    Adw.init()
    app = Shortmouse()
    return app.run([argv[0]])


if __name__ == "__main__":
    raise SystemExit(main())
