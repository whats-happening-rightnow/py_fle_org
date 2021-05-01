# py_fle_org

Organizes files from source directory to another using the destination directory's sub-folder names as keywords.

First execution will move matched files into a "staging" folder for review.

Subsequent executions will first detect if there are files in the staging folder and offer to move to final destination.

Usage:

Populate `config.py` file:

* `SOURCE_FOLDERS` = folders where files to be moved located, multiple folders separated with a pipe `|`
* `DESTINATION_FOLDER` = destination folders where files are to be moved,  multiple folders separated with a pipe `|`
* `IGNORE_DESTINATION_FOLDER` = any sub-folders at destination location that should be ignored,  multiple folders separated with a comma `,`
* `STAGE_FOLDER` = folder where files should be moved prior to moving to final destination - for review - specificy one location only

Once config done, run: `python fleorg.py`
