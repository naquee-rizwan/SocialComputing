"""
    http://snap.stanford.edu/snappy/index.html

    Snap.py is a Python interface for SNAP. SNAP is a general purpose, high performance system for analysis and
    manipulation of large networks. SNAP is written in C++ and optimized for maximum performance and compact graph
    representation. It easily scales to massive networks with hundreds of millions of nodes, and billions of edges.

    Snap.py provides performance benefits of SNAP, combined with flexibility of Python. Most of the SNAP functionality
    is available via Snap.py in Python.

    The latest version of Snap.py is 6.0 (Dec 28, 2020), available for macOS, Linux, and Windows 64-bit. This version
    is a major release with a large number of new features, most notably a significantly improved way to call Snap.py
    functions in Python, a NetworkX compatibility layer, standard Python functions to handle SNAP vector and hash
    types, new functions for egonets and graph union, and a completely revised package building infrastructure with a
    better support for various versions of Python (see Release Notes for details). These enhancements are backward
    compatible, so existing Snap.py based programs should continue to work.
"""

status = False

try:
    import snap
    version = snap.Version
    i = snap.TInt(5)
    if i == 5:
        status = True
except:
    pass

if status:
    print("SUCCESS, your version of Snap.py is %s" %(version))
else:
    print("*** ERROR, no working Snap.py was found on your computer")