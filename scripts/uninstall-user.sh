#!/usr/bin/env bash
set -euo pipefail
PREFIX="${HOME}/.local"
rm -rf "${PREFIX}/share/shortmouse"
rm -f "${PREFIX}/bin/shortmouse"
rm -f "${PREFIX}/share/applications/shortmouse.desktop"
if command -v update-desktop-database >/dev/null; then
  update-desktop-database -q "${PREFIX}/share/applications" || true
fi
if command -v gsettings >/dev/null; then
  schema="org.gnome.settings-daemon.plugins.media-keys"
  path="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/shortmouse/"
  gsettings set ${schema}.custom-keybinding:${path} name ""
  gsettings set ${schema}.custom-keybinding:${path} command ""
  gsettings set ${schema}.custom-keybinding:${path} binding ""
fi
echo "Removed shortmouse from ${PREFIX}"
