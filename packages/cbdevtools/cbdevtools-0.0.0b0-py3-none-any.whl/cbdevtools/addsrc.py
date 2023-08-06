#!/usr/bin/env python3

###
# ????
###


from pathlib import Path
import sys


###
# prototype::
#     file    = ; // See Python typing...
#               ???
#     project = ; // See Python typing...
#               ???
###

def addsrc(
    file   : str,
    project: str,
) -> None:
    project_dir = Path(file).parent

    if not project in str(project_dir):
        raise Exception(
            "call the script from a working directory containing the project."
        )

    while(not project_dir.name.startswith(project)):
        project_dir = project_dir.parent

    sys.path.append(str(MODULE_DIR))
