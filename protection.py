# -*- coding: utf-8 -*-
from math import sqrt, pow, sin, pi
from FreeCAD import Base
import Part
import Drawing


# Settings
docName = "CopterProtection";
copterWidth = 552;
screwDiameter = 255;
screwSpace = 5;
protectionWidth = 20;
plasticHeight = 2;
centerRectHoleWidth = 100;
centerRectOutlineWidth = 15;
connLineWidth = 15;

debug = 0;


# Cleanup from previous run
for doc in App.listDocuments():
	if doc == docName:
		App.closeDocument(doc);

App.newDocument(docName);

# Some calculations
cylinderOffset = sqrt(pow(copterWidth/2, 2)/2);
smallCylRadius = screwDiameter / 2 + screwSpace;
bigCylRadius = smallCylRadius + protectionWidth;
connLineOffset = cylinderOffset + (smallCylRadius + screwSpace / 2) * sin((120 - 45)*pi/180);

print cylinderOffset;
print connLineOffset;

res = Part.Face(Part.Wire(Part.makeCircle(bigCylRadius, Base.Vector(-cylinderOffset, -cylinderOffset, 0))));

res = res.fuse(Part.makePlane(cylinderOffset * 2, connLineWidth,
	Base.Vector(-cylinderOffset, -connLineOffset - connLineWidth / 2, 0)));
res = res.removeSplitter();

res = res.fuse(Part.Face(Part.Wire(Part.makeCircle(bigCylRadius, Base.Vector(+cylinderOffset, -cylinderOffset, 0)))));
res = res.removeSplitter();

res = res.fuse(Part.makePlane(connLineWidth, cylinderOffset * 2,
	Base.Vector(connLineOffset - connLineWidth / 2, -cylinderOffset, 0)));
res = res.removeSplitter();

res = res.fuse(Part.Face(Part.Wire(Part.makeCircle(bigCylRadius, Base.Vector(+cylinderOffset, +cylinderOffset, 0)))));
res = res.removeSplitter();

res = res.fuse(Part.makePlane(cylinderOffset * 2, connLineWidth,
	Base.Vector(-cylinderOffset, connLineOffset - connLineWidth / 2, 0)));
res = res.removeSplitter();

res = res.fuse(Part.Face(Part.Wire(Part.makeCircle(bigCylRadius, Base.Vector(-cylinderOffset, +cylinderOffset, 0)))));
res = res.removeSplitter();

res = res.fuse(Part.makePlane(connLineWidth, cylinderOffset * 2,
	Base.Vector(-connLineOffset - connLineWidth / 2, -cylinderOffset, 0)));
res = res.removeSplitter();

tmp = connLineWidth / sqrt(2) / 2;
res = res.fuse(Part.Face(Part.Wire(Part.makePolygon([
	Base.Vector(-cylinderOffset + tmp, -cylinderOffset - tmp, 0),
	Base.Vector(-cylinderOffset - tmp, -cylinderOffset + tmp, 0),
	Base.Vector(+cylinderOffset - tmp, +cylinderOffset + tmp, 0),
	Base.Vector(+cylinderOffset + tmp, +cylinderOffset - tmp, 0),
	Base.Vector(-cylinderOffset + tmp, -cylinderOffset - tmp, 0)
]))));
res = res.removeSplitter();
res = res.fuse(Part.Face(Part.Wire(Part.makePolygon([
	Base.Vector(-cylinderOffset - tmp, +cylinderOffset - tmp, 0),
	Base.Vector(-cylinderOffset + tmp, +cylinderOffset + tmp, 0),
	Base.Vector(+cylinderOffset + tmp, -cylinderOffset + tmp, 0),
	Base.Vector(+cylinderOffset - tmp, -cylinderOffset - tmp, 0),
	Base.Vector(-cylinderOffset - tmp, +cylinderOffset - tmp, 0)
]))));
res = res.removeSplitter();

tmp = centerRectHoleWidth + centerRectOutlineWidth * 2;
res = res.fuse(Part.makePlane(tmp, tmp, Base.Vector(-tmp / 2, -tmp / 2, 0)));
res = res.removeSplitter();

res = res.cut(Part.Face(Part.Wire(Part.makeCircle(smallCylRadius, Base.Vector(-cylinderOffset, -cylinderOffset, 0)))));
res = res.cut(Part.Face(Part.Wire(Part.makeCircle(smallCylRadius, Base.Vector(-cylinderOffset, +cylinderOffset, 0)))));
res = res.cut(Part.Face(Part.Wire(Part.makeCircle(smallCylRadius, Base.Vector(+cylinderOffset, -cylinderOffset, 0)))));
res = res.cut(Part.Face(Part.Wire(Part.makeCircle(smallCylRadius, Base.Vector(+cylinderOffset, +cylinderOffset, 0)))));

tmp = centerRectHoleWidth;
res = res.cut(Part.makePlane(tmp, tmp, Base.Vector(-tmp / 2, -tmp / 2, 0)));

cutLength = 0;
for wire in res.Wires:
	for edge in wire.Edges:
		cutLength += edge.Length;

matherialArea = res.Area;

res = res.extrude(Base.Vector(0, 0, plasticHeight));

Part.show(res);

fullArea = res.BoundBox.XLength * res.BoundBox.YLength;

#if debug == 1:
	#res = Part.Line(Base.Vector(-cylinderOffset, -cylinderOffset, 0), Base.Vector(-cylinderOffset, +cylinderOffset)).toShape();
	#res = res.fuse(Part.Line(Base.Vector(-cylinderOffset, -cylinderOffset, 0), Base.Vector(+cylinderOffset, -cylinderOffset)).toShape());
	#res = res.fuse(Part.Line(Base.Vector(+cylinderOffset, +cylinderOffset, 0), Base.Vector(-cylinderOffset, +cylinderOffset)).toShape());
	#res = res.fuse(Part.Line(Base.Vector(+cylinderOffset, +cylinderOffset, 0), Base.Vector(+cylinderOffset, -cylinderOffset)).toShape());
	#res = res.fuse(Part.Line(Base.Vector(+cylinderOffset, +cylinderOffset, 0), Base.Vector(-cylinderOffset, -cylinderOffset)).toShape());
	#res = res.fuse(Part.Line(Base.Vector(+cylinderOffset, -cylinderOffset, 0), Base.Vector(-cylinderOffset, +cylinderOffset)).toShape());
	#Part.show(res);

Gui.ActiveDocument.ActiveView.fitAll();

# Draw result
App.ActiveDocument.addObject("Drawing::FeaturePage", "Page");
App.ActiveDocument.Page.Template = App.getResourceDir() + "Mod/Drawing/Templates/A4_Portrait_1_english.svg";
#App.ActiveDocument.Page.Template = App.getResourceDir() + "Mod/Drawing/Templates/A4_Landscape.svg";

App.ActiveDocument.Page.EditableTexts = [
	u'1 : 5',
	u'Screw protector',
	u'RoboClub@GL',
	u'Denys Kuzmenko',
	u'none',
	u'07/15/12',
	u'01',
	u'001 - 001',
	u'ISO2768 - fH',
	u'PVC Foam / Styrofoam'];

App.ActiveDocument.addObject("Drawing::FeatureViewPart", "View");
App.ActiveDocument.View.Source = App.ActiveDocument.Shape;
App.ActiveDocument.View.Scale = 0.2;
App.ActiveDocument.View.Direction = (0.0, 0.0, 1.0);
App.ActiveDocument.View.X = 105;
App.ActiveDocument.View.Y = 100;

App.ActiveDocument.Page.addObject(App.ActiveDocument.View);

App.activeDocument().addObject('Drawing::FeatureView','ViewSelf')
App.activeDocument().ViewSelf.ViewResult = """
<text x="20" y="185" font-size = "5">Cut lenght: """ + str(cutLength / 1e3) + """ m</text>
<text x="20" y="190" font-size = "5">Used area: """ + str(matherialArea / 1e6) + """ <tspan baseline-shift = "super">m2</tspan></text>
<text x="20" y="195" font-size = "5">Full area: """ + str(fullArea / 1e6) + """ <tspan baseline-shift = "super">m2</tspan></text>
<text x="20" y="200" font-size = "5">Usage effectiveness: """ + str(matherialArea * 100/ fullArea) + """%</text>
<text x="20" y="205" font-size = "5">Center rect. size: 100mm</text>
"""
#<text x="20" y="205" font-size = "5">Scale: 1:5</text>

App.activeDocument().Page.addObject(App.activeDocument().ViewSelf)

App.ActiveDocument.recompute();
