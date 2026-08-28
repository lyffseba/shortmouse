"""Walk AT-SPI and collect on-screen clickable widgets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import gi

gi.require_version("Atspi", "2.0")
from gi.repository import Atspi  # noqa: E402

SKIP_APPS = {
    "gnome-shell",
    "gsd-keyboard",
    "gsd-color",
    "gsd-wacom",
    "gsd-media-keys",
    "gsd-power",
    "gsd-xsettings",
    "ibus-extension-gtk3",
    "ibus-x11",
    "xdg-desktop-portal-gtk",
    "xdg-desktop-portal-gnome",
    "evolution-alarm-notify",
    "update-notifier",
    "org.gnome.Software",
    "gjs",
    "shortmouse",
    "reach",
}

CLICK_ROLES = {
    "push button",
    "toggle button",
    "menu item",
    "check menu item",
    "radio menu item",
    "page tab",
    "link",
    "radio button",
    "check box",
    "combo box",
    "slider",
    "heading",
}

PER_APP = 150
MAX_TOTAL = 500


@dataclass
class Target:
    label: str
    title: str
    app: str
    role: str
    x: int
    y: int
    w: int
    h: int
    accessible: Any


def _role(obj) -> str:
    try:
        return obj.get_role_name() or ""
    except Exception:
        return ""


def _name(obj) -> str:
    try:
        return (obj.get_name() or "").strip()
    except Exception:
        return ""


def _n_actions(obj) -> int:
    try:
        return int(obj.get_n_actions())
    except Exception:
        return 0


def _action_name(obj, index: int) -> str:
    try:
        return obj.get_action_name(index) or ""
    except Exception:
        return ""


def _showing(obj) -> bool:
    try:
        st = obj.get_state_set()
        return st.contains(Atspi.StateType.SHOWING)
    except Exception:
        return False


def click(obj) -> None:
    n = _n_actions(obj)
    if n <= 0:
        try:
            obj.grab_focus()
        except Exception:
            pass
        return
    names = [_action_name(obj, i) for i in range(n)]
    skip = {"window.close", "window.minimize", "close", "minimize"}
    for want in (
        "click",
        "press",
        "doDefault",
        "default.activate",
        "activate",
        "window.raise",
    ):
        if want in names:
            obj.do_action(names.index(want))
            return
    for i, name in enumerate(names):
        if name not in skip:
            obj.do_action(i)
            return


def _add(found, seen, app_name, obj, role, name, x, y, w, h) -> None:
    key = (app_name, role, name, x, y, w, h)
    if key in seen:
        return
    seen.add(key)
    found.append(
        Target(
            label="",
            title=name,
            app=app_name,
            role=role,
            x=x,
            y=y,
            w=w,
            h=h,
            accessible=obj,
        )
    )


def scan() -> list[Target]:
    desktop = Atspi.get_desktop(0)
    found: list[Target] = []
    seen: set[tuple] = set()
    total = 0

    for i in range(desktop.get_child_count()):
        app = desktop.get_child_at_index(i)
        if app is None:
            continue
        app_name = _name(app) or "app"
        if app_name in SKIP_APPS:
            continue
        app_nodes = 0

        def visit(obj, depth: int) -> None:
            nonlocal total, app_nodes
            if obj is None or depth > 14 or total >= MAX_TOTAL or app_nodes >= PER_APP:
                return
            total += 1
            app_nodes += 1
            role = _role(obj)
            name = _name(obj)
            nact = _n_actions(obj)
            x = y = w = h = 0
            try:
                ext = obj.get_extents(Atspi.CoordType.SCREEN)
                x, y, w, h = ext.x, ext.y, ext.width, ext.height
            except Exception:
                pass

            if role in {"frame", "window"} and name:
                _add(found, seen, app_name, obj, "window", name, x, y, w, h)
            elif name and nact and role in CLICK_ROLES:
                showing = _showing(obj)
                is_menu = "menu" in role
                if showing or is_menu:
                    _add(found, seen, app_name, obj, role, name, x, y, w, h)

            try:
                count = obj.get_child_count()
            except Exception:
                return
            cap = 80 if depth < 3 else 40
            for j in range(min(count, cap)):
                try:
                    child = obj.get_child_at_index(j)
                except Exception:
                    continue
                visit(child, depth + 1)

        visit(app, 0)

    # windows first, then the rest
    found.sort(key=lambda t: (0 if t.role == "window" else 1, t.app, t.title.lower()))
    return found
