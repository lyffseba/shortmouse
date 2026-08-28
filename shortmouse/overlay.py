"""Fullscreen letter overlay (original; not a fork of hints)."""

from __future__ import annotations

from typing import Callable

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gdk, GLib, Gtk, Pango, PangoCairo  # noqa: E402

from shortmouse.atspi_scan import Target, click

CSS = b"""
window.shortmouse-overlay {
  background-color: alpha(black, 0.18);
}
"""


class OverlayWindow(Gtk.Window):
    def __init__(self, targets: list[Target], on_done: Callable[[], None]):
        super().__init__(title="shortmouse")
        self.add_css_class("shortmouse-overlay")
        self.set_decorated(False)
        self.set_resizable(True)
        self._targets = targets
        self._typed = ""
        self._on_done = on_done

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.area = Gtk.DrawingArea()
        self.area.set_hexpand(True)
        self.area.set_vexpand(True)
        self.area.set_draw_func(self._draw)
        self.set_child(self.area)

        keys = Gtk.EventControllerKey()
        keys.connect("key-pressed", self._on_key)
        self.add_controller(keys)

        self.fullscreen()
        self.connect("close-request", lambda *_: self._finish())

    def _visible(self) -> list[Target]:
        if not self._typed:
            return self._targets
        return [t for t in self._targets if t.label.startswith(self._typed)]

    def _draw(self, _area, cr, width: int, height: int) -> None:
        cr.set_source_rgba(0, 0, 0, 0.18)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        layout = PangoCairo.create_layout(cr)
        desc = Pango.FontDescription("Sans Bold 11")
        layout.set_font_description(desc)

        for target in self._visible():
            text = target.label
            rest = text[len(self._typed) :]
            shown = self._typed.upper() + rest.upper() if self._typed else text.upper()
            layout.set_text(shown, -1)
            tw, th = layout.get_pixel_size()
            pad_x, pad_y = 6, 3
            box_w, box_h = tw + pad_x * 2, th + pad_y * 2
            x = max(0, min(width - box_w, target.x + 2))
            y = max(0, min(height - box_h, target.y + 2))

            cr.set_source_rgb(1.0, 0.835, 0.290)  # shortmouse yellow
            _round_rect(cr, x, y, box_w, box_h, 4)
            cr.fill()
            cr.set_source_rgb(0.12, 0.10, 0.05)
            cr.move_to(x + pad_x, y + pad_y)
            PangoCairo.show_layout(cr, layout)

    def _on_key(self, _c, keyval, _code, _state) -> bool:
        if keyval == Gdk.KEY_Escape:
            self._finish()
            return True
        if keyval == Gdk.KEY_BackSpace:
            self._typed = self._typed[:-1]
            self.area.queue_draw()
            return True
        if keyval == Gdk.KEY_Return:
            vis = self._visible()
            if len(vis) == 1:
                self._pick(vis[0])
            return True
        ch = Gdk.keyval_to_unicode(keyval)
        if not ch:
            return False
        letter = chr(ch).lower()
        if letter not in "abcdefghijklmnopqrstuvwxyz":
            return False
        candidate = self._typed + letter
        matches = [t for t in self._targets if t.label.startswith(candidate)]
        if not matches:
            return True
        self._typed = candidate
        if len(matches) == 1:
            self._pick(matches[0])
        else:
            self.area.queue_draw()
        return True

    def _pick(self, target: Target) -> None:
        self.hide()
        GLib.idle_add(self._click_and_finish, target)

    def _click_and_finish(self, target: Target) -> bool:
        click(target.accessible)
        self._finish()
        return False

    def _finish(self) -> None:
        self.close()
        self._on_done()


def _round_rect(cr, x, y, w, h, r) -> None:
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -1.57, 0)
    cr.arc(x + w - r, y + h - r, r, 0, 1.57)
    cr.arc(x + r, y + h - r, r, 1.57, 3.14)
    cr.arc(x + r, y + r, r, 3.14, 4.71)
    cr.close_path()
