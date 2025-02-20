
import os
import shutil
import getpass
import datetime

import bpy

from publish import utils


def source():
    """
    get saved blender file path
    """
    source_filpath = bpy.data.filepath

    return source_filpath


def usd_export(selected, animation, uvmaps, materials, filepath=None):

    filepath = filepath or utils.getTempFilepath(".usda")

    result = bpy.ops.wm.usd_export(
        selected_objects_only = selected,
        visible_objects_only = False,
        export_animation  = animation,
        export_hair = False,
        export_uvmaps = uvmaps,
        export_normals = False,
        export_materials = materials,
        generate_preview_surface = False,
        export_textures = False,
        overwrite_textures = False,
        relative_paths = False,
        use_instancing = False,
        filepath=filepath,
    )

    if "FINISHED" not in result:
        return None
    
    return filepath


def alembic_export(selected, hair, particles, filter_alembic, filepath=None):

    filepath = filepath or utils.getTempFilepath(".abc")

    result = bpy.ops.wm.alembic_export(
        selected = selected,
        visible_objects_only = False,
        export_hair=hair, 
        export_particles = particles,        
        filter_alembic = filter_alembic,
        face_sets=False,
        filter_text=False,
        filter_blenlib=False,
        filter_usd=False,
        subdiv_schema=False,
        filepath=filepath,
    )
    
    if "FINISHED" not in result:
        return None
    
    return filepath


def mp4_export(file_format, video_format, frame_start, frame_end, fps, filepath=None):

    filepath = filepath or utils.getTempFilepath(".mp4")

    # Set render settings
    bpy.context.scene.render.image_settings.file_format = file_format
    bpy.context.scene.render.ffmpeg.format = video_format
    bpy.context.scene.render.ffmpeg.codec = "H264"
    bpy.context.scene.render.ffmpeg.audio_codec = "AAC" 
    bpy.context.scene.render.ffmpeg.video_bitrate = 8000  # Setting default values

    # Set resolution and frame rate
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.fps = fps  # set the frames per sec

    # Set frame range
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

    # Set output file path
    bpy.context.scene.render.filepath = filepath

    # Render the animation
    result = bpy.ops.render.render(animation=True)

    if "FINISHED" not in result:
        return None
    
    return filepath

def mov_export(file_format, video_format, frame_start, frame_end, fps, filepath=None):

    filepath = filepath or utils.getTempFilepath(".mov")

    # Set render settings
    bpy.context.scene.render.image_settings.file_format = file_format
    bpy.context.scene.render.ffmpeg.format = video_format
    bpy.context.scene.render.ffmpeg.codec = "H264"
    bpy.context.scene.render.ffmpeg.audio_codec = "AAC" 
    bpy.context.scene.render.ffmpeg.video_bitrate = 8000  # Setting default values

    # Set resolution and frame rate
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.fps = fps  # set the frames per sec

    # Set frame range
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

    # Set output file path
    bpy.context.scene.render.filepath = filepath

    # Render the animation
    result = bpy.ops.render.render(animation=True)

    if "FINISHED" not in result:
        return None
    
    return filepath


def register(category, name, department, typed):

    current_version = utils.getCurrentVersion(category, name, department, typed)
    next_version = utils.nextVersion(current_version)

    # version context
    version_context = {
        "name": name, # monkey
        "category": category, #Asset or shot
        "department": department, # modelling, rigging, etc
        "version": next_version,
        "comment": "test publish",
        "project": utils.getProjectName(),
        "type": typed,
        "status": None,
        "createAt": datetime.datetime.now().strftime("%Y/%m/%d - %I:%M"),
        "createBy": getpass.getuser(),
    }

    utils.writeJson(version_context)

    return version_context


def deployed(source_filpath, target_filepath):

    if not os.path.exists(os.path.dirname(target_filepath)):
        os.makedirs(
            os.path.dirname(target_filepath)
        )
    # This is the exact clone of the user saved file
    shutil.copy(source_filpath, target_filepath)



