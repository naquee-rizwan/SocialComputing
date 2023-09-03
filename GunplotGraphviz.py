"""
    http://snap.stanford.edu/snappy/index.html

    Snap.py supports Python 2.x and Python 3.x on macOS, Linux, and Windows 64-bit.
    Snap.py requires that Python is installed on your machine.
    Make sure that your operating system is 64-bit and that your Python is a 64-bit version.

    Snap.py is self-contained, it does not require any additional packages for its basic functionality. However,
    it requires external packages to support plotting and visualization functionality. The following packages need to
    be installed in addition to Snap.py, if you want to use plotting and visualizations in Snap.py:

    Gnuplot [http://www.gnuplot.info/] for plotting structural properties of networks (e.g., degree distribution);
    Graphviz [https://www.graphviz.org/] for drawing and visualizing small graphs.
    Set the system PATH variable, so that Gnuplot and Graphviz are available, or put their
    executables in the working directory.
"""


import snap

graph_gen_pref_attach = snap.GenPrefAttach(100000, 3)
graph_gen_pref_attach.PlotInDegDistr("pref-attach", "PrefAttach(100000, 3) in Degree")

graph = snap.GenGrid(snap.PUNGraph, 5, 3)
graph.DrawGViz(snap.gvlDot, "grid5x3.png", "Grid 5x3")
