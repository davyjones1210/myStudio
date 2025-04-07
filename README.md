# myStudio
Pipeline rapid training with Subin Gopi


`myStudio` is a pipeline training package designed to help artists and developers rapidly learn and implement production pipelines for animation and VFX projects. This package provides tools and utilities for asset management, scene assembly, publishing workflows, and more, with a focus on integrating with Autodesk Maya.

---

## Features

- **Asset Management**: Tools to manage assets, including referencing, versioning, and metadata handling.
- **Scene Assembly**: Automate the assembly of animation and lighting scenes using Alembic caches, lookdev shaders, and metadata.
- **Publishing Workflows**: Streamline the process of exporting and publishing assets, including Alembic files and Maya scenes.
- **PySide Windows**: Custom PySide-based UI windows for user interaction and workflow automation.
- **Integration with Maya**: Seamless integration with Autodesk Maya for asset referencing, shader assignments, and scene exports.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/myStudio.git

2. Add the myStudio package to your Python path:

3. Ensure Autodesk Maya is installed and the required plugins (e.g., AbcExport, mtoa) are loaded.


## Usage

1. Scene Assembly
The myStudio package automates the process of assembling scenes for animation and lighting. It references Alembic caches, lookdev shaders, and metadata to connect shaders to geometry.

Example:
from myStudio.assemble import main

main.assembleLighting(
    start_frame=1001,
    end_frame=1020,
    category="shot",
    name="shot-101",
    department="lighting",
    typed="sourcefile",
    assets=["main_cam", "alien", "pyramid", "dobby"]
)


2. Publishing Workflows
The myStudio package provides tools to export Alembic files and publish assets.

Example:
from myStudio.publish import maya_scene

maya_scene.maya_alembic_export_per_asset(
    frame_start=1001,
    frame_end=1020,
    directory="C:/projects/exports"
)

3. PySide Windows
myStudio includes custom PySide-based UI windows for user interaction. These windows simplify workflows such as asset selection, versioning, and publishing.



## Requirements
Autodesk Maya (2022 or later)
Python 3.7+
PySide2 or PySide6
Maya Plugins:
AbcExport (for Alembic exports)
mtoa (for Arnold shaders)

## Folder Structure

myStudio/
├── assemble/
│   ├── __init__.py
│   ├── main.py
├── publish/
│   ├── __init__.py
│   ├── maya_scene.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
├── screenshots/
│   ├── asset_manager_window.png
│   ├── scene_assembly_window.png
│   ├── publishing_window.png
└── [README.md](http://_vscodecontentref_/2)

## Contributing
We welcome contributions to improve the myStudio package. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.


## Acknowledgments

Special thanks to Subin Gopi for providing guidance and training on pipeline development.