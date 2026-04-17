import bpy

addon_keymaps = []


def add_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is None:
        return

    km = kc.keymaps.new(name="Sequencer", space_type="SEQUENCE_EDITOR")

    kmi = km.keymap_items.new("scene.superinsertar", type="Y", value="PRESS", ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new("scene.superanimar", type="Q", value="PRESS", ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("scene.sobreponeraudio", "O", "PRESS", ctrl=True, shift=True)
    kmi.properties.macros = True
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("scene.superaliniar", type="R", value="PRESS", ctrl=True, shift=False)
    kmi.properties.macros = True
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("scene.superzoon", type="P", value="PRESS", ctrl=True, shift=False)
    kmi.properties.macros = True
    kmi.properties.incrementro = False
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("scene.superzoon", type="U", value="PRESS", ctrl=True, shift=False)
    kmi.properties.macros = True
    kmi.properties.incrementro = True
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("scene.moverclip", type="J", value="PRESS", ctrl=True, shift=False)
    kmi.properties.macros = True
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("scene.hueva", "U", "PRESS", ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))


def remove_hotkey():
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except RuntimeError:
            pass
    addon_keymaps.clear()
