

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


# Brightway packages

import bw2data as bd
from bw2io.importers.ecospold2_biosphere import Ecospold2BiosphereImporter
from bw2io.importers.ecospold2 import SingleOutputEcospold2Importer
from bw2io.migrations import create_core_migrations
from bw2io.importers.ecoinvent_lcia import EcoinventLCIAImporter
class BrightwayProjectSetup:


    def __init__(self, project_name:str):
        self.project_name = project_name
        self.foreground_db = None
        
        bd.projects.set_current(self.project_name)
        print(f"Active project: {bd.projects.current}")
        create_core_migrations()
        

    def setup_biosphere(self, biosphere_db_name:str, bg_db_path:str,version:str):
         ##this sets up a code for the migrations from biosphere
                        ## essential for the excel importer function to apply strategies

    
        if biosphere_db_name not in bd.databases:
            biosphere_db=Ecospold2BiosphereImporter(name=biosphere_db_name, version=version, 
                                            filepath=os.path.join(bg_db_path, "MasterData", "ElementaryExchanges.xml"))
            biosphere_db.apply_strategies()
            biosphere_db.statistics()
            biosphere_db.write_database()
        else:
            print(f"{biosphere_db_name} is are already installed.")

    def setup_methods(self, biosphere_db_name:str=None,method_dir:str=None,methods_version:str=None):

        if len(bd.methods) == 0: ##only execute if no methods are in the methods dictionary 
            methods = EcoinventLCIAImporter(biosphere_database=biosphere_db_name, dir_path=method_dir, 
                                            methods_version=methods_version)
            methods.apply_strategies()
            methods.statistics()
            methods.write_methods(overwrite=True)
            print(len(bd.methods))
        else:
            print("LCIA methods are already installed.")
    
    def setup_background_database(self, bg_db_name:str, bg_db_path:str, biosphere_db_name:str):
        if bg_db_name not in bd.databases:
            ecoinvent_db=SingleOutputEcospold2Importer(dirpath=os.path.join(bg_db_path,"datasets"), 
                                                    db_name=bg_db_name,
                                                    biosphere_database_name=biosphere_db_name, 
                                                    use_mp=False)
            ecoinvent_db.apply_strategies()
            ecoinvent_db.statistics()
            ecoinvent_db.write_database()
        else:
            print(f"{bg_db_name} is already installed.")

    
