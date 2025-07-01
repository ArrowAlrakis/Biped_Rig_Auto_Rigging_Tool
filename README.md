# Biped_AutoRig_Python_Tool
[Final Rig Preview](./Preview.png)

Python Auto Rig Tool for Biped Characters  
Created by Arrow Lyu. Designed for humanoid and two-legged creature characters.

# Main Scripts

📄 [Biped_AutoRig_Python_Tool.py](./Biped_AutoRig_Python_Tool.py) – Contains the core rigging functions used to build the biped auto rig.  
📄 [Biped_AutoRig_Creation.py](./Biped_AutoRig_Creation.py) – The main runnable script that sets up and builds the rig for a specific character.

# Overview
This is a Python-based Auto Rigging Tool for biped characters in Autodesk Maya.  
Originally developed for a stylized humanoid character (`RigSuitMan`), the tool can be adjusted to work with other humanoid or bipedal creatures with similar proportions.

It generates joint chains, FK/IK controllers, and constraints, forming a clean and animator-friendly rig that is ready for skin weight painting.

# Key Features

- Auto joint chain setup for spine, arms, legs, and neck  
- FK/IK controls for arms and legs  
- Modular function layout for easier customization  
- Adjustable naming, joint counts, and structure in script  
- Scripted entirely in Python (Maya `cmds`)  
- Designed to work inside Maya (tested in 2019–2025)

# Demo  
▶ Watch the full biped auto-rig demo: [Watch on Vimeo](https://vimeo.com/1097249142/81bcc98230)

(Note: This script is built using Python and structured modularly. Some techniques are inspired by tools developed by my instructor, Dennis Turner, but only my own code is included in this repository.)

# How to Use

1. Open your biped model in Maya  
2. Run `Biped_AutoRig_Creation.py` in Maya's script editor  
3. Adjust joint positions or tweak naming conventions as needed in script  
4. Let the script build the full rig  
5. Proceed with skin weight painting and animation

# Notes

- This is a hardcoded tool intended for quick personal or project-based rigging.
- The code is organized for clarity, and users with basic scripting knowledge can customize body proportions, naming, or control styles.
- Originally designed for a humanoid character but extendable to other bipeds.

# About the Author
This rigging tool was developed by Arrow Lyu, a game artist and character rigger with a strong interest in technical art. This tool reflects hands-on experience building animation-ready rigs through Python scripting.

# Contact / Portfolio
Email: jcrane@gmail.com  
GitHub: [[Arrow's profile]](https://github.com/ArrowAlrakis)
