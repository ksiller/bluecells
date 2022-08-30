from ij import IJ, Prefs
from ij.plugin import ChannelSplitter, ImageCalculator
from ij.plugin.frame import RoiManager


imp = IJ.getImage()
rm = RoiManager.getRoiManager()

Prefs.blackBackground = True
mask = imp.duplicate()
IJ.run(mask, "Median...", "radius=10")
IJ.run(mask, "8-bit", "")
IJ.setAutoThreshold(mask, "Default dark")
IJ.run(mask, "Convert to Mask", "")
IJ.run(mask, "Analyze Particles...", "size=10000-Infinity circularity=0.50-1.00") 
fov = rm.getRoisAsArray()
if len(fov) > 0:
    mask.setRoi(fov[0])
    IJ.run(mask, "Clear Outside", "");
mask.show()

imp2 = imp.duplicate()
channels = ChannelSplitter.split(imp2)
blue = ImageCalculator.run(channels[2], channels[0], "Subtract create");
blue.show();

blue_mask = blue.duplicate()
blue_mask.show()

Prefs.blackBackground = False
IJ.run(blue_mask, "Median...", "radius=0.5")
IJ.setAutoThreshold(blue_mask, "Moments dark");
IJ.run(blue_mask, "Convert to Mask", "");
IJ.run(blue_mask, "Analyze Particles...", "size=20-500 show=Overlay exclude clear display overlay add");
