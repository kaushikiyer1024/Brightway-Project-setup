# Brightway-Project-setup



A straightforward, reusable Python class to quickly initialize a [Brightway2](https://brightway.dev/) Life Cycle Assessment (LCA) project directly from local `ecospold2` files (like the ecoinvent database).

Setting up Brightway databases from raw XML directories can sometimes be a headache of pathing and sequential imports. This script abstracts the heavy lifting into a simple, three-step pipeline: Biosphere -> Methods -> Background Database.

Features
* Automatically creates or connects to a specified Brightway project.
* Imports the Biosphere database and applies core migrations.
* Installs standard LCIA methods.
* Imports an unlinked background database (e.g., ecoinvent 3.x) from local `.xml` directories.
* Checks if databases already exist to prevent redundant, time-consuming imports.

Prerequisites

Before using this script, you must have the following installed:
* Python 3.8+
* `brightway25` (specifically `bw2data` and `bw2io`)

You will also need **local copies** of your background database in `ecospold2` format. For ecoinvent, this means downloading the `7z` or `zip` file of the unlinked database from their website and extracting it. 

This code also has the functionality to extract and write custom versions of the characterization methods. bw2io and EcoinventLCIAImporter by default uses v3.9 of the characterization methods but if you want to use updated versions, it is possible. You only have to make these following changes to your brightway installation and codebase: 


An example usage of this package is shown in trial_project_setup.py


As of 2026-03-25


*If you have installed brightway using an anaconda environment, go to Directory/anaconda/envs/*env_name*/Lib/site-packages/bw2io/data and replace the existing _init_.py file with the _init_.py in this github repository. 


*In *Directory*/anaconda/envs/*env_name*/Lib/site-packages/bw2io/importers, replace the ecoinvent_lcia.py file with the ecoinvent_lcia.py file in this repo. 


If you want to use the default characterization methods by bw2io, then you dont need to update any library files, you can directly save project_setup.py in your project directory and use it.  

The extracted folder should contain at least two subfolders:
* `MasterData/` (contains `ElementaryExchanges.xml`)
* `datasets/` (contains the thousands of individual `.xml` activity files)
