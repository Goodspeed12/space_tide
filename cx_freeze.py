import os
from cx_Freeze import setup, Executable

#os.chdir(r"C:\Users\kozlo\Documents\python nauka\pcs_projekt")

buildOptions = dict(include_files = ['pcs_projekt/']) #folder,relative path. Use tuple like in the single file to set a absolute path.

setup(
         name = "SpaceTide",
         version = "1.0",
         description = "description",
         author = "pawlo",
         options = dict(build_exe = buildOptions),
         executables = [Executable("pcs_projekt/game_all_in_one.py")])