# @ Integer (label="Cell min area", min=1, max=1000) cell_min
# @ Integer (label="Cell max area", min=1, max=1000) cell_max

from ij import IJ, Prefs
from ij.gui import Overlay
from ij.plugin import ChannelSplitter, ImageCalculator
from ij.plugin.frame import RoiManager


def get_fov_mask(imp):
    Prefs.blackBackground = True
    mask = imp.duplicate()
    IJ.run(mask, "Median...", "radius=10")
    IJ.run(mask, "8-bit", "")
    IJ.setAutoThreshold(mask, "Default dark")
    IJ.run(mask, "Convert to Mask", "")
    print (imp.getWidth(), imp.getHeight(), imp.getWidth() * imp.getHeight())
    min_fov_area = int(imp.getWidth() * imp.getHeight() / 4)
    IJ.run("Set Measurements...", "area mean min centroid integrated display redirect=None")
    IJ.run(mask, "Analyze Particles...", "size=" + str(min_fov_area) + "-Infinity circularity=0.50-1.00 add") 
    fov = rm.getRoisAsArray()
    if len(fov) > 0:
        mask.setRoi(fov[0])
        IJ.setBackgroundColor(0, 0, 0)
        IJ.run(mask, "Clear Outside", "")
    return mask

def get_cell_masks(imp, mask):
    imp2 = imp.duplicate()
    channels = ChannelSplitter.split(imp2)
    blue = ImageCalculator.run(channels[2], channels[0], "Subtract create")
    blue = ImageCalculator.run(blue, mask, "And create")
    #blue.show()

    cell_mask = blue.duplicate()
    #cell_mask.show()

    rm.reset()
    Prefs.blackBackground = False
    IJ.run(cell_mask, "Median...", "radius=0.5")
    IJ.setAutoThreshold(cell_mask, "MaxEntropy dark")
    IJ.run(cell_mask, "Convert to Mask", "")
    IJ.run(cell_mask, "Watershed", "")
    return cell_mask

def measure(imp, cell_mask, minsize, maxsize):    
    IJ.run("Set Measurements...", "area mean min centroid integrated display redirect="+imp.getTitle()+" decimal=3")
    IJ.run(cell_mask, "Analyze Particles...", "size=" + str(minsize) + "-" + str(maxsize) + " show=Overlay exclude display overlay add")
    return rm.getRoisAsArray()

def add_overlay(imp, rois):
    overlay = Overlay()
    for roi in rois:
        overlay.add(roi)
    imp.setOverlay(overlay)

imp = IJ.getImage()
rm = RoiManager.getRoiManager()
rm.reset()
fov = get_fov_mask(imp)
blue_cell_mask = get_cell_masks(imp, fov)
rois = measure(imp, blue_cell_mask, cell_min, cell_max)
add_overlay(imp, rois) 

