import pandas as pd
import numpy as np
import itk_pdb.dbAccess as dbAccess
import os
from datetime import datetime
from itk_pdb.dbAccess import ITkPDSession
import itk_pdb.dbAccess as dbAccess
import json
import logging
import os
import time
import coloredlogs
import sys
from pathlib import Path

import itkdb
#klappt so
def eos_test(filename, sn, code):
        client = itkdb.Client(use_eos=True)

        filename = filename  

        data = {"component": code,
                "title": "%s before Ni-coating"%sn,
                "description": "Picture before Ni-coating",
                "url": Path(filename),
                "type": "file"}
        attachment = {"data": open(filename, 'rb')}


        with Path(filename).open("rb") as fpointer:
                files = {"data": itkdb.utils.get_file_components({"data": fpointer})}  
                response = client.post("createComponentAttachment", data=data, files=files)  

#eos_test("BaseBloc_1-0001-0090(2).jpg", "20UPBBB0000002", "c7f81310557d253e167458d4591ab80c")
