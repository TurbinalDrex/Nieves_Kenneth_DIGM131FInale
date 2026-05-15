# Nieves_Kenneth_DIGM131FInale
Safe Cleanup Pipeline Tool:-
Code that Deletes history and Freezes Transforms (With options for NOT deleting Non-deformer History)

Tool Is Designed for animators, riggers, and modelers who need safer scene scleanup operations without accidentally breaking rigs or deformational systems.

-PLANNED FEATURES-

(Week 6) Core Features _ COMPLETED

(Week 7) Data-Driven Config System _ COMPLETED

(Week 7) Error handling + Debug Mode _ WIP

(Week 9) Maya UI window _ WIP

(Week 9) JSON Save/Load Presets _ WIP

(Week 10) Polish/Documentation _ WIP

-STRUCTURE OF PROJECT-

Safe_Cleanup_Tool/

Config_Data.py          # Core Cleanups Functions (BASIC cmds Logic)
Data_Driven_Config.py   # Preset Configs (Data-Driven Settings)
main.py                 # Entry Point For Running the Tool
README.md               # Project Doc

-Functions I NEED to write-

freeze_transforms(obj_name)

delete_non_deformer_history(obj_name)

delete_all_history(obj_name)

safe_cleanup(obj_name)

-HOW TO RUN-

1. Load project folder into maya's script path
2. select an object in scene
3. run 'main.py'
4. Tool will perform a safe cleanup on selected object
