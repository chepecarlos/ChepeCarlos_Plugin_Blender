BLENDER ?= /home/chepecarlos/5.Programas/1.Edicion/1.Blender/blender-5.1.1-linux-x64/blender
PROJECT_ROOT ?= /home/chepecarlos/5.Programas/1.Edicion
ADDON_MODULE ?= ALSW_Plugin_Blender
DIST_DIR ?= dist
BLENDER_CONFIG_VERSION ?= 5.1
ADDONS_DIR ?= $(HOME)/.config/blender/$(BLENDER_CONFIG_VERSION)/scripts/addons
ZIP_NAME ?= $(ADDON_MODULE)-$(shell date +%Y%m%d-%H%M%S).zip

.PHONY: blenderaddon blenderaddon-dev blenderaddon-bg blenderaddon-check zip zlip install-local

blenderaddon:
	$(BLENDER) --factory-startup --python-expr "import sys; sys.path.insert(0, '$(PROJECT_ROOT)'); import $(ADDON_MODULE) as addon; addon.register()"

blenderaddon-dev:
	$(BLENDER) --python-expr "import sys, importlib; sys.path.insert(0, '$(PROJECT_ROOT)'); import $(ADDON_MODULE) as addon; importlib.reload(addon); addon.register(); print('ADDON_DEV_LOADED')"

blenderaddon-bg:
	$(BLENDER) --background --factory-startup --python-expr "import sys; sys.path.insert(0, '$(PROJECT_ROOT)'); import $(ADDON_MODULE) as addon; addon.register(); print('REGISTER_OK'); addon.unregister(); print('UNREGISTER_OK')"

blenderaddon-check:
	$(BLENDER) --background --factory-startup --python-expr "import bpy; print(bpy.app.version_string)"

zip:
	mkdir -p "$(DIST_DIR)"
	zip -r "$(DIST_DIR)/$(ZIP_NAME)" . \
		-x ".git/*" \
		-x ".mypy_cache/*" \
		-x "__pycache__/*" \
		-x "operaciones/__pycache__/*" \
		-x "$(DIST_DIR)/*"
	@echo "ZIP listo en $(DIST_DIR)/$(ZIP_NAME)"

zlip: zip

install-local:
	mkdir -p "$(ADDONS_DIR)/$(ADDON_MODULE)"
	rsync -a --delete \
		--exclude ".git/" \
		--exclude ".mypy_cache/" \
		--exclude ".vscode/" \
		--exclude "__pycache__/" \
		--exclude "operaciones/__pycache__/" \
		--exclude "$(DIST_DIR)/" \
		./ "$(ADDONS_DIR)/$(ADDON_MODULE)/"
	@echo "Addon instalado en $(ADDONS_DIR)/$(ADDON_MODULE)"