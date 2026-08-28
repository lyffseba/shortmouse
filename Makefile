.PHONY: help dump run install-user uninstall-user

help:
	@echo "shortmouse — letter hints for Linux GUIs"
	@echo
	@echo "  make dump            List AT-SPI click targets"
	@echo "  make run             Show the overlay"
	@echo "  make install-user    App menu + Super+Shift+Space"
	@echo "  make uninstall-user  Remove the user install"

dump:
	PYTHONPATH=. python3 -m shortmouse --dump

run:
	PYTHONPATH=. python3 -m shortmouse

install-user:
	./scripts/install-user.sh

uninstall-user:
	./scripts/uninstall-user.sh
