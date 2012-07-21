# -*- coding: utf-8 -*-
from math import sqrt, pow, sin, pi
from FreeCAD import Base
import Part
import Drawing


# Settings
docName = "CopterProtection_Mod";
plasticHeight = 6;
centerRectHoleWidth = 100;

centerHoleRect0Width = 90.5;
centerHoleRect45Width = 80;
centerHoleSpokeWidth = 42;
centerHoleCurveRadius = 0.5;

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


res = Part.makePlane(centerHoleRect0Width, centerHoleSpokeWidth,
	Base.Vector(-centerHoleRect0Width / 2, -centerHoleSpokeWidth / 2, 0));
res = res.fuse(Part.makePlane(centerHoleSpokeWidth, centerHoleRect0Width,
	Base.Vector(-centerHoleSpokeWidth / 2, -centerHoleRect0Width / 2, 0)));
res = res.removeSplitter();

res = res.fuse(Part.Face(Part.Wire(Part.makePolygon([
	Base.Vector(0, -sqrt(2) * centerHoleRect45Width / 2, 0),
	Base.Vector(+sqrt(2) * centerHoleRect45Width / 2, 0, 0),
	Base.Vector(0, +sqrt(2) * centerHoleRect45Width / 2, 0),
	Base.Vector(-sqrt(2) * centerHoleRect45Width / 2, 0, 0),
	Base.Vector(0, -sqrt(2) * centerHoleRect45Width / 2, 0),
]))).common(Part.makePlane(centerHoleRect0Width, centerHoleRect0Width,
	Base.Vector(-centerHoleRect0Width / 2, -centerHoleRect0Width / 2, 0))));
res = res.removeSplitter();

res = Part.makePlane(centerRectHoleWidth, centerRectHoleWidth,
	Base.Vector(-centerRectHoleWidth / 2, -centerRectHoleWidth / 2, 0)).cut(res);
res = res.removeSplitter();

cutLength = 0;
for wire in res.Wires:
	for edge in wire.Edges:
		cutLength += edge.Length;

matherialArea = res.Area;

res = res.extrude(Base.Vector(0, 0, plasticHeight));

Part.show(res);

fullArea = res.BoundBox.XLength * res.BoundBox.YLength;

Gui.ActiveDocument.ActiveView.fitAll();

# Draw result
App.ActiveDocument.addObject("Drawing::FeaturePage", "Page");
App.ActiveDocument.Page.Template = App.getResourceDir() + "Mod/Drawing/Templates/A4_Portrait_1_english.svg";
#App.ActiveDocument.Page.Template = App.getResourceDir() + "Mod/Drawing/Templates/A4_Landscape.svg";

App.ActiveDocument.Page.EditableTexts = [
	u'1 : 1',
	u'Screw protector (Mod)',
	u'RoboClub@GL',
	u'Denys Kuzmenko',
	u'none',
	u'07/18/12',
	u'01',
	u'001 - 002',
	u'ISO2768 - fH',
	u'PVC Foam / Styrofoam'];

App.ActiveDocument.addObject("Drawing::FeatureViewPart", "View");
App.ActiveDocument.View.Source = App.ActiveDocument.Shape;
App.ActiveDocument.View.Scale = 1;
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
<text x="20" y="205" font-size = "5">Outer rect. size: 100mm</text>
"""
#<text x="20" y="205" font-size = "5">Scale: 1:5</text>

App.activeDocument().Page.addObject(App.activeDocument().ViewSelf)

App.ActiveDocument.recompute();
