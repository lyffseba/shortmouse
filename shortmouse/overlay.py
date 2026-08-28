"""Visible letter HUD. GNOME Wayland cannot host a transparent overlay
without a Shell extension, so this is a real always-on-top window.
"""

from __future__ import annotations

from typing import Callable

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")
from gi.repository import Adw, Gdk, GLib, Gtk, Pango  # noqa: E402

from shortmouse.atspi_scan import Target, click

CSS = b"""
window.shortmouse-hud {
  background-color: #1b1b1b;
}
.shortmouse-chip {
  background-color: #ffd54a;
  color: #1a1408;
  font-weight: 800;
  font-family: monospace;
  padding: 2px 8px;
  border-radius: 6px;
  min-width: 28px;
}
.shortmouse-title {
  font-size: 14px;
}
"""


class OverlayWindow(Adw.ApplicationWindow):
    def __init__(self, application, targets: list[Target], on_done: Callable[[], None]):
        super().__init__(application=application, title="shortmouse")
        self.add_css_class("shortmouse-hud")
        self.set_default_size(560, 520)
        self.set_resizable(True)
        self._all = targets
        self._typed = ""
        self._on_done = on_done
        self._rows: list[Target] = []

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        toolbar = Adw.ToolbarView()
        header = Adw.HeaderBar()
        title = Gtk.Label(label="shortmouse")
        title.add_css_class("title")
        header.set_title_widget(title)
        toolbar.add_top_bar(header)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(8)
        box.set_margin_bottom(12)
        box.set_margin_start(14)
        box.set_margin_end(14)

        self.hint = Gtk.Label(xalign=0)
        self.hint.add_css_class("dim-label")
        self.hint.set_wrap(True)
        box.append(self.hint)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type the yellow letters…")
        self.entry.connect("changed", self._on_typed)
        self.entry.connect("activate", lambda *_: self._activate_first())
        box.append(self.entry)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.add_css_class("boxed-list")
        self.listbox.connect("row-activated", lambda *_: self._activate_selected())
        scrolled.set_child(self.listbox)
        box.append(scrolled)

        self.empty = Gtk.Label(
            label="No matches. GTK apps (Terminal, Files, Settings) work best.",
            xalign=0,
        )
        self.empty.add_css_class("dim-label")
        self.empty.set_wrap(True)
        box.append(self.empty)

        toolbar.set_content(box)
        self.set_content(toolbar)

        keys = Gtk.EventControllerKey()
        keys.connect("key-pressed", self._on_key)
        self.add_controller(keys)
        self.connect("close-request", lambda *_: self._finish() or False)
        self.connect("map", lambda *_: self.entry.grab_focus())
        self._render()

    def _matches(self) -> list[Target]:
        q = (self._typed or "").lower()
        if not q:
            return list(self._all)
        out = []
        for t in self._all:
            blob = f"{t.label} {t.title} {t.app}".lower()
            if t.label.startswith(q) or q in blob:
                out.append(t)
        return out

    def _on_typed(self, entry: Gtk.Entry) -> None:
        self._typed = (entry.get_text() or "").strip().lower()
        self._render()
        matches = self._matches()
        letter_hits = [t for t in matches if t.label.startswith(self._typed)] if self._typed else []
        if self._typed and len(letter_hits) == 1 and self._typed == letter_hits[0].label:
            self._pick(letter_hits[0])

    def _on_key(self, _c, keyval, _code, _state) -> bool:
        if keyval == Gdk.KEY_Escape:
            self._finish()
            return True
        if keyval == Gdk.KEY_Down:
            self._move(1)
            return True
        if keyval == Gdk.KEY_Up:
            self._move(-1)
            return True
        return False

    def _move(self, delta: int) -> None:
        row = self.listbox.get_selected_row()
        rows = []
        i = 0
        while True:
            r = self.listbox.get_row_at_index(i)
            if r is None:
                break
            rows.append(r)
            i += 1
        if not rows:
            return
        idx = rows.index(row) if row in rows else 0
        idx = max(0, min(len(rows) - 1, idx + delta))
        self.listbox.select_row(rows[idx])

    def _render(self) -> None:
        while True:
            row = self.listbox.get_row_at_index(0)
            if row is None:
                break
            self.listbox.remove(row)

        matches = self._matches()
        self._rows = matches
        n = len(self._all)
        if n == 0:
            self.hint.set_text(
                "No clickable widgets in the focused app. Try Files, Settings, or Terminal."
            )
        else:
            self.hint.set_text(
                f"{len(matches)} / {n}  ·  type yellow letters, or click a row. Esc cancels."
            )
        self.empty.set_visible(not matches)

        for target in matches[:80]:
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row_box.set_margin_top(8)
            row_box.set_margin_bottom(8)
            row_box.set_margin_start(10)
            row_box.set_margin_end(10)
            chip = Gtk.Label(label=target.label.upper())
            chip.add_css_class("shortmouse-chip")
            texts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            title = Gtk.Label(label=target.title, xalign=0)
            title.add_css_class("shortmouse-title")
            title.set_ellipsize(Pango.EllipsizeMode.END)
            sub = Gtk.Label(label=f"{target.role} · {target.app}", xalign=0)
            sub.add_css_class("dim-label")
            sub.set_ellipsize(Pango.EllipsizeMode.END)
            texts.append(title)
            texts.append(sub)
            row_box.append(chip)
            row_box.append(texts)
            row = Gtk.ListBoxRow()
            row.set_child(row_box)
            self.listbox.append(row)

        if matches:
            first = self.listbox.get_row_at_index(0)
            if first:
                self.listbox.select_row(first)

    def _activate_first(self) -> None:
        if self._rows:
            self._pick(self._rows[0])

    def _activate_selected(self) -> None:
        row = self.listbox.get_selected_row()
        if row is None:
            return
        idx = row.get_index()
        if 0 <= idx < len(self._rows):
            self._pick(self._rows[idx])

    def _pick(self, target: Target) -> None:
        self.hide()
        GLib.timeout_add(80, self._click_and_finish, target)

    def _click_and_finish(self, target: Target) -> bool:
        click(target.accessible)
        self._finish()
        return False

    def _finish(self) -> bool:
        self.close()
        self._on_done()
        return True
