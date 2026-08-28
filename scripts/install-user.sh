#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PREFIX="${HOME}/.local"
BINDIR="${PREFIX}/bin"
SHARE="${PREFIX}/share/shortmouse"
APPS="${PREFIX}/share/applications"
BIN="${BINDIR}/shortmouse"
DESKTOP="${APPS}/shortmouse.desktop"

mkdir -p "$BINDIR" "$SHARE" "$APPS"
rm -rf "${SHARE}/shortmouse"
cp -a "${ROOT}/shortmouse" "${SHARE}/shortmouse"
install -m 0644 "${ROOT}/packaging/shortmouse.desktop" "$DESKTOP"
sed -i "s|^Exec=.*|Exec=${BIN}|" "$DESKTOP"

cat > "$BIN" <<EOF
#!/bin/sh
export PYTHONPATH="${SHARE}\${PYTHONPATH:+:\$PYTHONPATH}"
exec python3 -m shortmouse "\$@"
EOF
chmod 0755 "$BIN"

if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate "$DESKTOP"
fi
if command -v update-desktop-database >/dev/null; then
  update-desktop-database -q "$APPS" || true
fi

if command -v gsettings >/dev/null; then
  schema="org.gnome.settings-daemon.plugins.media-keys"
  path="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/shortmouse/"
  existing="$(gsettings get ${schema} custom-keybindings)"
  if ! grep -q "custom-keybindings/shortmouse/" <<<"$existing"; then
    if [[ "$existing" == "@as []" || "$existing" == "[]" ]]; then
      gsettings set ${schema} custom-keybindings "['${path}']"
    else
      trimmed="${existing%]}"
      gsettings set ${schema} custom-keybindings "${trimmed}, '${path}']"
    fi
  fi
  # Super+Shift+Space — same chord as Shortcat on a Mac (Cmd+Shift+Space)
  gsettings set ${schema}.custom-keybinding:${path} name "shortmouse"
  gsettings set ${schema}.custom-keybinding:${path} command "${BIN}"
  gsettings set ${schema}.custom-keybinding:${path} binding "<Super><Shift>space"
  # do not fight ourselves: drop that chord from older experiments
  for old in hints reach; do
    oldpath="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/${old}/"
    current="$(gsettings get ${schema}.custom-keybinding:${oldpath} binding 2>/dev/null || echo '')"
    if [[ "$current" == "'<Super><Shift>space'" ]]; then
      gsettings set ${schema}.custom-keybinding:${oldpath} binding ""
    fi
  done
fi

echo
echo "shortmouse installed."
echo "  command : shortmouse"
echo "  shortcut: Super+Shift+Space"
echo "  menu    : shortmouse"
echo "  remove  : make uninstall-user"
