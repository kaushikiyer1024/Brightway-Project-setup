

import os
import inspect
from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
# Brightway packages
import bw2io as bi

import bw2data as bd
from bw2io.importers.ecospold2_biosphere import Ecospold2BiosphereImporter
from bw2io.importers.ecospold2 import SingleOutputEcospold2Importer
from bw2io.migrations import create_core_migrations
from bw2io.importers.ecoinvent_lcia import EcoinventLCIAImporter

class BrightwayProjectSetup:


    def __init__(self, project_name:str):

        stack=inspect.stack()
        caller_frame=stack[1]
        caller_filename=caller_frame.filename
        self.caller_dir=Path(caller_filename).parent.resolve()
        print(f"BrightwayProjectSetup was called from: {self.caller_dir}")
        self.project_name = project_name
        
        bd.projects.set_current(self.project_name)
        print(f"Active project: {bd.projects.current}")
        create_core_migrations()
        

    def setup_biosphere(self, biosphere_db_name:str, bg_db_path:str,version:str):
         ##this sets up a code for the migrations from biosphere
                        ## essential for the excel importer function to apply strategies

    
        if biosphere_db_name not in bd.databases:
            print('Installing biosphere database...')
            biosphere_db=Ecospold2BiosphereImporter(name=biosphere_db_name, version=version, 
                                            filepath=os.path.join(bg_db_path, "MasterData", "ElementaryExchanges.xml"))
            biosphere_db.apply_strategies()
            biosphere_db.statistics()
            biosphere_db.write_database()
            return biosphere_db
        else:
            print(f"{biosphere_db_name} is already installed.")
            return None

    def setup_methods(self, biosphere_db_name:str,method_dir:str,methods_version:str):

        if biosphere_db_name not in bd.databases:
            raise RuntimeError(f"Biosphere database '{biosphere_db_name}' not found. Run setup_biosphere first.")

        if not method_dir:
            raise ValueError('Method directory not defined.')

        if not methods_version:
            raise ValueError('Methods version not defined.')

        if len(bd.methods) == 0: ##only execute if no methods are in the methods dictionary 
            print('Installing local LCIA methods...')
            methods = EcoinventLCIAImporter(biosphere_database=biosphere_db_name, dir_path=method_dir, 
                                            methods_version=methods_version)
            methods.apply_strategies()
            methods.statistics()
            methods.write_methods(overwrite=True)
            print(len(bd.methods))
            return methods
        else:
            print("LCIA methods are already installed.")
            return None
    
    def setup_background_database(self, bg_db_name:str, bg_db_path:str, biosphere_db_name:str):
        if biosphere_db_name not in bd.databases:
            raise RuntimeError(f"Biosphere database '{biosphere_db_name}' not found. Run setup_biosphere first.")
        if bg_db_name not in bd.databases:
            print(f"Installing background database '{bg_db_name}'...")

            ecoinvent_db=SingleOutputEcospold2Importer(dirpath=os.path.join(bg_db_path,"datasets"), 
                                                    db_name=bg_db_name,
                                                    biosphere_database_name=biosphere_db_name, 
                                                    use_mp=False)
            ecoinvent_db.apply_strategies()
            ecoinvent_db.statistics()
            ecoinvent_db.write_database()
            ecoinvent_db_class=bd.Database(bg_db_name)
            return ecoinvent_db_class
        else:
            print(f"{bg_db_name} is already installed.")
            return bd.Database(bg_db_name)

    def setup_excel_database(self, 
                             database_path: str,
                             biosphere_db_name: str = 'biosphere3', 
                             bg_db_name: Optional[str] = None
                            ):
        print(bd.databases)
        # It is safer to require a background database name rather than assuming  a default.
        if bg_db_name is None:
            bg_db_name='ecoinvent-v3.9-cutoff'
            print(f"Warning: No background database name provided. Defaulting to '{bg_db_name}'.")
                
        if biosphere_db_name not in bd.databases:
            raise RuntimeError(f"Biosphere database '{biosphere_db_name}' not found. Run setup_biosphere first.")
        
        if bg_db_name not in bd.databases:
            raise RuntimeError(f"Background database '{bg_db_name}' not found. Run setup_background_database first.")
        
        try:
            foreground_database = pd.read_excel(io=database_path)
            db_info_row = foreground_database[foreground_database.iloc[:, 0].str.contains('database', case=False, na=False)]
            if db_info_row.empty:
                raise ValueError("Could not find a row with 'database' in the first column.")
            database_name = db_info_row.iloc[0, 1]
        except (IOError, ValueError, IndexError) as e:
            print(f"Error reading database name from Excel file '{database_path}': {e}")
            # Fallback to inferring name from the file path
            database_name = Path(database_path).stem.replace('_LCI', '')
            print(f"Attempting to use inferred database name: '{database_name}'")

        if database_path==None:
            database_path=os.path.join(self.caller_dir, 'LCA databases', f'{database_name}_LCI.xlsx')
            
        if database_name not in bd.databases:
            print(f"Importing and installing foreground '{database_name}' database. ")
            foreground_excel_database=bi.ExcelImporter(database_path)
            foreground_excel_database.apply_strategies()
            required_databases=set()
            for activity in foreground_excel_database.data:
                for exc in activity.get('exchanges',[]):
                    db_name=exc.get('database')
                    if db_name:
                        required_databases.add(db_name)

            print(f'Detected dependenices for {database_name}: {required_databases}\n')

            required_databases.discard(database_name)
            missing_databases=set(required_databases)-set((bd.databases))
            
            if missing_databases:
                raise ValueError(f'Install {missing_databases} first before installing {database_name}') 
            
            for db_name in required_databases:
                if db_name not in list(bd.databases):
                    raise ValueError(f'{db_name} not in the list of installed brightway databases in your project. Install ')
                print(f'Attempting to match dependcies against: {db_name}...')

                foreground_excel_database.match_database(db_name, fields=['name', 'unit', 'categories', 'location', 'reference product'])
            
            foreground_excel_database.statistics()
            unlinked_exchanges=len(list(foreground_excel_database.unlinked
                                            ))
            if unlinked_exchanges==0:
            
                foreground_excel_database.write_database()
                print(f"Successfully imported '{database_name}' with no unlinked exchanges.")
            else:
                print(f"Warning: Imported '{database_name}' with {unlinked_exchanges} unlinked exchanges. Check the logs for details.")
                foreground_excel_database.write_excel(database_name)
            
            foreground_database_class=bd.Database(database_name)
            return foreground_database_class, database_name
        else:
            print(f"{database_name} is already installed.")
            return bd.Database(database_name), database_name
