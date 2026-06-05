# Nieves_Kenneth_DIGM131FInale
Safe Cleanup Pipeline Tool:-
Code that Deletes history and Freezes Transforms (With options for NOT deleting Non-deformer History)

Tool Is Designed for animators, riggers, and modelers who need safer scene scleanup operations without accidentally breaking rigs or deformational systems.


-PLANNED FEATURES-

(Week 6) Core Features _ COMPLETED

(Week 7) Data-Driven Config System _ COMPLETED

(Week 7) Error handling + Debug Mode _ COMPLETED

(Week 9) Maya UI window _ COMPLETED

(Week 9) JSON Save/Load Presets _ COMPLETED

(Week 10) Polish/Documentation _ COMPLETED


-STRUCTURE OF PROJECT-

Safe_Cleanup_Tool/

Config_Data.py          # Core Cleanups Functions (BASIC cmds Logic)

Data_Driven_Config.py   # Preset Configs (Data-Driven Settings)

main.py                 # Entry Point For Running the Tool

README.md               # Project Doc

-Issues Still need to fix/Maybe Add-
Defmormer still being adjusted when using safe mode
Possible Options to close window when done with tool
a quick shelf button that Does safe mode regardless without the UI

-HOW TO RUN-

1. Copy the folder:
   BasicMayaCleanUpTool_KennethNieves

2. Paste into:
   Documents/maya/2026/scripts/

3. Open Maya Script Editor (Python mode) (NOT MEL)

4. Run:

import BasicMayaCleanUpTool_KennethNieves.main as main

main.launch_ui()
