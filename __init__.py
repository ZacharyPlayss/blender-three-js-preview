import bpy
import webbrowser
import os
from .webserver import PreviewServer

server = None

addon_folder = os.path.dirname(__file__)
web_folder = os.path.join(addon_folder, "webserver")
modelfolder = os.path.join(web_folder, "assets", "models")
os.makedirs(modelfolder, exist_ok=True)


class TOGGLE_THREEJS_SERVER_OT_operator(bpy.types.Operator):
    """Start or Stop THREE.js Preview Server"""
    bl_idname = "wm.toggle_threejs_server"
    bl_label = "Start Server"

    def execute(self, context):
        global server
        if server:
            server.stopServer()
            server = None
            self.report({'INFO'}, "THREE.js server stopped.")
        else:
            server = PreviewServer(8080, web_folder)
            server.startServer()
            webbrowser.open("http://localhost:8080")
            self.report({'INFO'}, "THREE.js server started at http://localhost:8080")
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
            export_apply=True,
            use_visible= True
        )
        self.report({'INFO'}, f"Scene exported to {filepath}. Refresh your browser preview manually.")
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
        global server
        if server:
            layout.operator("wm.toggle_threejs_server", text="Stop Server", icon="CANCEL")
        else:
            layout.operator("wm.toggle_threejs_server", text="Start Server", icon="PLAY")
        layout.operator("wm.export_scene_glb", text="Export Scene", icon="EXPORT")


def register():
    bpy.utils.register_class(TOGGLE_THREEJS_SERVER_OT_operator)
    bpy.utils.register_class(EXPORT_SCENE_OT_glb)
    bpy.utils.register_class(THREEJS_PT_panel)


def unregister():
    global server
    if server:
        server.stopServer()
        server = None
    bpy.utils.unregister_class(TOGGLE_THREEJS_SERVER_OT_operator)
    bpy.utils.unregister_class(EXPORT_SCENE_OT_glb)
    bpy.utils.unregister_class(THREEJS_PT_panel)


if __name__ == "__main__":
    register()
