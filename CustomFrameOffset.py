import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import IntProperty, BoolProperty

bl_info = {
    "name": "Custom Frame Offset",
    "author": "Fahad Hasan Pathik CGVIRUS",
    "version": (1, 0),
    "blender": (4, 40, 0),
    "description": "Offsets the timeline left/right with custom shortcuts following a given delta",
    "category": "Animation",
    "wiki_url": "https://github.com/cgvirus/blender-Custom-Frame-Offset-addon",
}

addon_keymaps = []

# ------------------------------------------------------------------------
# Operators
# ------------------------------------------------------------------------

class OFFSET_OT_Left(Operator):
    """Offset the timeline to the left"""
    bl_idname = "offset.left"
    bl_label = "Offset Left"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        if scene.custom_frame_offset:
            bpy.ops.screen.frame_offset(delta=-scene.custom_frame_offset_delta)
        return {'FINISHED'}


class OFFSET_OT_Right(Operator):
    """Offset the timeline to the right"""
    bl_idname = "offset.right"
    bl_label = "Offset Right"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        if scene.custom_frame_offset:
            bpy.ops.screen.frame_offset(delta=scene.custom_frame_offset_delta)
        return {'FINISHED'}

# ------------------------------------------------------------------------
# Add-on Preferences with Keymap Instructions
# ------------------------------------------------------------------------

class OffsetAddonPreferences(AddonPreferences):
    """Add-on preferences panel for keybinding instructions"""
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout

        # Instructions for changing keybindings
        layout.label(text="Custom Shortcut Keys:")
        layout.label(text="1. Go to Edit > Preferences > Keymap")
        layout.label(text="2. Search for 'Offset Left' or 'Offset Right'")
        layout.label(text="3. Edit keybindings as needed")

        layout.separator()

        # Button to open Preferences panel for keymap changes
        layout.operator("wm.preferences", text="Open Preferences")

# ------------------------------------------------------------------------
# UI Draw Functions
# ------------------------------------------------------------------------

def draw_frame_offset_delta(self, context):
    """Draw the custom frame offset delta property"""
    layout = self.layout
    scene = context.scene

    if scene.custom_frame_offset:
        layout.prop(context.scene, 'custom_frame_offset_delta', text="Delta")

def draw_frame_offset_toggle(self, context):
    """Draw the custom frame offset toggle"""
    layout = self.layout
    layout.prop(context.scene, 'custom_frame_offset', text="Use Custom Offset")

# ------------------------------------------------------------------------
# Keymap Registration
# ------------------------------------------------------------------------

def register_keymaps():
    """Register default keymaps for the add-on"""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type='EMPTY')

        # Default keymaps for the offset operators
        kmi_left = km.keymap_items.new("offset.left", 'LEFT_ARROW', 'PRESS', ctrl=True)
        kmi_right = km.keymap_items.new("offset.right", 'RIGHT_ARROW', 'PRESS', ctrl=True)

        addon_keymaps.append((km, [kmi_left, kmi_right]))

def unregister_keymaps():
    """Unregister keymaps for the add-on"""
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        for km, kmi_list in addon_keymaps:
            for kmi in kmi_list:
                km.keymap_items.remove(kmi)
            kc.keymaps.remove(km)
        addon_keymaps.clear()

# ------------------------------------------------------------------------
# Register & Unregister Add-on
# ------------------------------------------------------------------------

classes = (
    OFFSET_OT_Left,
    OFFSET_OT_Right,
    OffsetAddonPreferences,
)

def register():
    """Register classes, keymaps, and properties"""
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add properties to the scene
    bpy.types.Scene.custom_frame_offset_delta = IntProperty(
        name="Frame Offset",
        default=5,
        description="Amount to offset frames by"
    )
    bpy.types.Scene.custom_frame_offset = BoolProperty(
        name="Use Custom Offset",
        default=True,
        description="Enable or disable custom frame offsetting"
    )

    # Append custom UI elements to the Dopesheet and Playback tabs
    bpy.types.DOPESHEET_HT_header.append(draw_frame_offset_delta)
    bpy.types.TIME_PT_playback.append(draw_frame_offset_toggle)

    # Register default keymaps
    register_keymaps()

def unregister():
    """Unregister classes, keymaps, and properties"""
    unregister_keymaps()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Remove properties from the scene
    del bpy.types.Scene.custom_frame_offset_delta
    del bpy.types.Scene.custom_frame_offset

    # Remove custom UI elements from the Dopesheet and Playback tabs
    bpy.types.DOPESHEET_HT_header.remove(draw_frame_offset_delta)
    bpy.types.TIME_PT_playback.remove(draw_frame_offset_toggle)

if __name__ == "__main__":
    register()
