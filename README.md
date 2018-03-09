# LogInj
Logisim Circuit Injector

### Inputs
This python script requires exactly 3 inputs:
1) Destination file name
2) Source file name
3) Source file subcircuit name

### What it does
This file will first back up your logisim destination file. It then checks to see if the source file and destination file can be xml parsed and will parse them. It then checks to see if the source file's subscircuit exists, if it does it will copy it, if not it will just exit. Next it inserts the found circuit in the source file into the destination file and then saves it.

### How to use

`python inject.py dest.circ source.circ subcircuit`
