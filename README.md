# Code-Tilting-Paper

Python & Arduino scripts used in the rOoC paper.

Code-S1: Arduino code using Arduino 9-Axis motion shield to measure pitch & roll
Code-S2: Python scipt to plot pitch & roll
Code-S4: Python script to plot cell orientation histograms from vector fields
Code-S5: Python script to plot cell orientation histograms from contour files (from FIJI)
Code-S6: Python script for simplified flow model

Requires following packages (using pip install "package_name"):

- Matplotlib
- Numpy
- Glob
- Pandas
- Easygui
- OpenCV
- OS
- CSV

Following datasets are attached:
- Brightfield images of HUVECs processed with OrientationJ. Vector fields saved as CSV and imported in HistoFromOrientation.
- Confocal images of HUVECs cytosceleton processed with OrientationJ. Vector fields saved as CSV and imported in HistoFromOrientation.
- Nuclei from HUVECs filtered and analysed CellPose. Outline files later imported in Outline-Analyser and CSV files of Orientation analysed with HistoFromOrientation. 
