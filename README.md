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

The extracted folder should contain at least two subfolders:
* `MasterData/` (contains `ElementaryExchanges.xml`)
* `datasets/` (contains the thousands of individual `.xml` activity files)

## Installation

Clone this repository to your local machine:

```bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
