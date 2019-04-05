from ij import IJ, ImageStack, ImagePlus
from net.imglib2.meta import ImgPlus
from ij.plugin.frame import RoiManager
from ij.measure import ResultsTable, Measurements

IJ.run("Close All", "")
IJ.log("\\Clear")


imp = IJ.run("Bio-Formats Importer")
imp = IJ.getImage()

ch_1 = ImageStack(imp.width, imp.height)
ch_1.addSlice(str(1), imp.getProcessor(1))
imp.close()
ch1 = ImagePlus("ch1" + str(0), ch_1)
IJ.run(ch1, "Enhance Contrast", "saturated=0.35")
ch1.show()
raw_ch1 = ch1.duplicate()
IJ.setAutoThreshold(ch1, "IJ_IsoData dark")
IJ.run(ch1, "Analyze Particles...", "size=1000000-Infinity clear add")
rm = RoiManager.getInstance()
IJ.run(ch1, "Subtract Background...", "rolling=300")
IJ.run(ch1, "Gaussian Blur...", "sigma=7")
IJ.setAutoThreshold(ch1, "Triangle dark")
IJ.run(ch1, "Create Selection", "")
rm.addRoi(ch1.getRoi());
table = ResultsTable()

size = rm.getCount()
print size
for i in range(size-1):
	table.incrementCounter()

	roi = rm.getRoi(i)
	raw_ch1.setRoi(roi)
	stats = raw_ch1.getStatistics()

	rm.setSelectedIndexes([i,size-1])
	rm.runCommand(raw_ch1, "AND")
	rm.addRoi(raw_ch1.getRoi())
	roi = rm.getRoi(rm.getCount()+1)
	stats2 = raw_ch1.getStatistics()


	rm.setSelectedIndexes([i,rm.getCount()])
	rm.runCommand(raw_ch1, "XOR")
	rm.addRoi(raw_ch1.getRoi())
	roi = rm.getRoi(rm.getCount()+1)
	stats3 = raw_ch1.getStatistics()


	table.addValue("Area full section", stats.area)
	table.addValue("Sum of Intesity", stats.area*stats.mean)
	table.addValue("Mean Int Pixels", stats.mean)

	table.addValue("Area Foreground", stats2.area)
	table.addValue("Sum of Intesity Foreground", stats2.area*stats2.mean)
	table.addValue("Mean Int Pixels Foreground", stats2.mean)

	table.addValue("Area Background", stats3.area)
	table.addValue("Sum of Intesity Background", stats3.area*stats.mean)
	table.addValue("Mean Int Pixels Background", stats3.mean)


table.show("Results Analysis")
