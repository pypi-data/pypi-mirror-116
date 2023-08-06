# PMAgg

A matplotlib GUI backend with interactive capabilities.

#### Introduction

PMAgg is a matplotlib backend with richer interactive capabilities, based on PySide2.
It is currently integrated in the open source project [Pyminer](https://gitee.com/py2cn/pyminer), as the default drawing interface, in order to achieve a drawing window similar to matlab.

#### Usage

```python
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('module://PMAgg') # switch to PMAgg backend
x=np.linspace(0,2*np.pi,100)
y=x*np.sin(x)
plt.plot(x,y)
plt.show()
```

![](pmagg.png)

Basic function
====================

![](pmagg_api.png)

**Right-click function**: right-click on the curve, legend, text, rectangle, ellipse and other objects to delete the object or modify the style

**save**: Save the drawing in various image formats

**setting**: modify the axis, title, default font, grid, comment style selection

**home**: delete all additional elements, such as rectangles, notes, text, etc.

**front/back**: adjust back the graphics before and after panning

**zoom/pan**: select zoom and pan

**rotate**: 3D rotation, and six orientation views in toolbar 2

**text**: add text, support LaTeX formula

**rect/oval**: add rectangle and ellipse labels, display center coordinates and area, for measurement, etc.

**annotation**: add extra point annotations on the curve, you can make rich style modifications

**grid**: show or hide the grid

**legend**: show or hide the legend

**colormap**: modify the color style of the colorbar
