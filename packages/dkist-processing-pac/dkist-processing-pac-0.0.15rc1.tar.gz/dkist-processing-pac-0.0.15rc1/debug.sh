#!/bin/bash

# List of python commands
commands=(
    "from PAC_Pipeline import *"
    "from PAC_Pipeline.QA import *"
    "from PAC_Pipeline.M12 import *"
    "from PAC_Pipeline.utils import *"
    "import numpy as np"
    "from importlib import reload"
    "from astropy.io import fits as pyfits"
)

# Join with ';'
command_str=$(IFS=';' ; echo "${commands[*]}")

# Run python
python -i -c "${command_str}"