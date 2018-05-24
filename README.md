# py_gazedat

Python code for converting eye tracking data (.gazedata) with variable formats to a
uniform format, where variables are always stored under constant headers, column positions, data types and scales.
Script: standardizeGazedataAnon.py

The implementation is based on dedicated classes. Conversion from variable data formats is further based
on a headermap, which lists input headernames, new standard headernames, and starndardized column numbers. These must be given in 3 columns
separated by tab chars, respectively (e.g., "header map 3d.txt" within this repository).

Anonymization of data is also supported. This is based on erasing unique timestamps and assigning random names to datafiles and within data participant
idetifiers.
