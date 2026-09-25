# shortmouse

Keyboard letter hints for Linux. Hold the keys, type the letters, the
cursor goes there.

Inspired by [Shortcat](https://shortcat.app/) on macOS. Built as our
own open-source app for GNOME/Linux — not a port of Shortcat, and not
a fork of [hints](https://github.com/AlfredoSequeida/hints).

> **Not affiliated** with Shortcat, Sproutcube, or Chendo Enterprises.
> Shortcat® is their trademark. We liked the *job* (stay on the
> keyboard) and wrote original code.

Press **Super+Shift+Space**. Yellow labels appear on buttons, tabs,
and menus. Type `F` or `AS` to click that widget.

## Why this exists

Cursor ships no Linux Grok Bot. Apple ships no Shortcat for Linux.
People on GNOME still want to click without a mouse. **shortmouse**
is a small community tool for that.

GTK apps (Terminal, Files, Settings) expose real UI through AT-SPI,
so labels land on the right controls. Chromium / Electron often
expose almost nothing; those apps need their own accessibility.

## Install (GNOME)

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-atspi-2.0
git clone https://github.com/lyffseba/shortmouse.git
cd shortmouse
make install-user
```

Then **Super+Shift+Space**, or launch **shortmouse** from the app menu.

```bash
make uninstall-user
```

## Use

1. Focus the window you want to click in.
2. Super+Shift+Space.
3. Type the letters on a yellow chip. Esc cancels. Backspace undoes.

## Stack

[docs/STACK.md](docs/STACK.md) pins the Makefile, the desktop install,
the shell scripts, and the Python runtime to their current stable
manuals.

## Related work

- [Shortcat](https://shortcat.app/) — the macOS command palette that
  made this interaction famous.
- [hints](https://github.com/AlfredoSequeida/hints) — a mature Linux
  overlay (GPL-3). We learned that AT-SPI + an overlay is the right
  shape on Linux. shortmouse is original code under MIT.

## License

MIT. See [NOTICE.md](NOTICE.md).
