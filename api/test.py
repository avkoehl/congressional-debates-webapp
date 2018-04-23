#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess

word = "spain"

output = subprocess.check_output("/usr/bin/python3 frequency.py" + " " +  word + " " + str(8), shell=True)
print (output)
