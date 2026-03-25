from project_setup import BrightwayProjectSetup
import bw2data as bd

import os
ecoinvent_version: str='3.11'
ecoinvent_type:str='cutoff'
background_db: str=f"ecoinvent-{ecoinvent_version}-{ecoinvent_type}"
background_db_dir: str=os.path.join('B:\\',f'ecoinvent v{ecoinvent_version}',ecoinvent_type)
biosphere_db_name: str='ecoinvent 3.11-biosphere'
#method_file_name:str='Cut-off Cumulative LCIA v3.11.xlsx'
project_setup=BrightwayProjectSetup(project_name='setup trial')

project_setup.setup_biosphere(biosphere_db_name=biosphere_db_name,
                              bg_db_path=background_db_dir,
                              version=ecoinvent_version)
print(len(bd.methods))

# Instead of using the built-in method importer:
# project_setup.setup_methods(biosphere_db_name=biosphere_db_name)

# Use the new custom importer for local files

"""

local_lcia_filepath = os.path.join(background_db_path, method_file_name)
if len(bd.methods) == 0:
    print("Importing LCIA methods from local Excel file with fuzzy matching...")
    import_lcia_from_local_excel(filepath=local_lcia_filepath, biosphere_name=biosphere_db_name)
else:
    print("LCIA methods are already installed.")
"""
project_setup.setup_methods(biosphere_db_name=biosphere_db_name)

    
project_setup.setup_background_database(bg_db_name=background_db, 
                                        bg_db_path=background_db_dir,
                                        biosphere_db_name=biosphere_db_name)

print(bd.projects.current)
