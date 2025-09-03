bl_info = {
    "name": "THREE.js GLTF previewer",
    "blender": (3, 0, 0),
    "category": "3D View",
    "description": "Preview blender models in three.js for a smoother exporting experience.",
}

import bpy
import webbrowser
import os
from .webserver import PreviewServer

server = None

addon_folder = os.path.dirname(__file__)
web_folder = os.path.join(addon_folder, "webserver")
modelfolder = os.path.join(web_folder, "assets", "models")
os.makedirs(modelfolder, exist_ok=True)

class OPEN_THREEJS_PREVIEW_OT_operator(bpy.types.Operator):
    """Open THREE.js Preview"""
    bl_idname = "wm.open_threejs_preview"
    bl_label = "Open THREE.js Preview"

    def execute(self, context):
        global server
        if not server:
            server = PreviewServer(8080, web_folder)
            server.startServer()
        webbrowser.open("http://localhost:8080")
        return {'FINISHED'}

class EXPORT_SCENE_OT_glb(bpy.types.Operator):
    """Export Blender scene as GLB"""
    bl_idname = "wm.export_scene_glb"
    bl_label = "Export Scene as GLB"

    def execute(self, context):
        filename = "model.glb"
        filepath = os.path.join(modelfolder, filename)
        bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format='GLB',
            export_apply=True
        )
        self.report({'INFO'}, f"Scene exported to {filepath}. Please refresh your browser preview manually.")
        return {'FINISHED'}

class REFRESH_THREEJS_OT_operator(bpy.types.Operator):
    """Open THREE.js Preview Again"""
    bl_idname = "wm.refresh_threejs_preview"
    bl_label = "Open THREE.js Preview Again"

    def execute(self, context):
        webbrowser.open("http://localhost:8080")
        self.report({'INFO'}, "Browser preview opened. Refresh manually if already open.")
        return {'FINISHED'}

class THREEJS_PT_panel(bpy.types.Panel):
    """Panel in 3D View sidebar"""
    bl_label = "THREE.js Preview"
    bl_idname = "VIEW3D_PT_threejs_preview"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "THREE.js"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.open_threejs_preview")
        layout.operator("wm.export_scene_glb")
        layout.operator("wm.refresh_threejs_preview")

def register():
    bpy.utils.register_class(OPEN_THREEJS_PREVIEW_OT_operator)
    bpy.utils.register_class(EXPORT_SCENE_OT_glb)
    bpy.utils.register_class(REFRESH_THREEJS_OT_operator)
    bpy.utils.register_class(THREEJS_PT_panel)

def unregister():
    global server
    if server:
        server.stopServer()
        server = None
    bpy.utils.unregister_class(OPEN_THREEJS_PREVIEW_OT_operator)
    bpy.utils.unregister_class(EXPORT_SCENE_OT_glb)
    bpy.utils.unregister_class(REFRESH_THREEJS_OT_operator)
    bpy.utils.unregister_class(THREEJS_PT_panel)

if __name__ == "__main__":
    register()
