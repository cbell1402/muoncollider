import ROOT
import sys
import shutil
import math

from array import array
from ctypes import *

try:
    input = raw_input
except:
    pass

if len(sys.argv) < 3:
    print("Usage: converter.py input_file output_file")
    sys.exit(1)

phimin = math.pi/2
phimax = (2)*math.pi


inputFile = sys.argv[1]
outputFile = sys.argv[2]
#f = ROOT.TFile.Open(inputFile, "READ")


shutil.copyfile(inputFile, outputFile)

# f = ROOT.TGeoManager.Import(inputFile)
outputFile = ROOT.TFile.Open(outputFile, "UPDATE")

outputFile.ls()
g = outputFile.Get("default")
# print(g.Dump())
# sys.exit()


ROOT.gGeoManager.DefaultColors()
# ROOT.gGeoManager.SetPhiRange(phimin=0., phimax=270.)
# LL - Successfully changes phi range of object

# g.Dump()
# # for i in range(10):
# g.CdTop()
# print(g.GetCurrentNode())


# # To look at BeampipeInner_0
# g.CdDown(0)
# print(g.GetCurrentNode().Dump())

# # To look at BeampipeOuter_1
# g.CdTop()
# g.CdDown(1)
# print(g.GetCurrentNode().Dump())
# # print(g.IsInPhiRange())
# # To get the volume object inside of the node
# print(g.GetCurrentNode().GetVolume().Dump())

# # To look at Vertex_6
# g.CdTop()
# g.CdDown(6)

# print(g.GetCurrentNode().Dump())
# # print(g.GetCurrentNode().ls())
# # print(g.IsInPhiRange())
# # To get the volume object inside of the node
# print(g.GetCurrentNode().GetVolume().Dump())
# g.CdDown(0)

# print(g.GetCurrentNode().Dump())


# print()
# print()
# print()
# print()
# print()

g.CdTop()
# print(g.GetListOfVolumes())
g.Dump()

vol = g.GetMasterVolume()
print(vol.GetNdaughters() )
print(vol.GetNodes() )


def getGlobalLocation(node):
    print("in new function", node.GetName())
    parentCoords=array('d', [-1,-1,-1])
    node.LocalToMaster(node.GetVolume().GetShape().GetOrigin(), parentCoords)
    print(parentCoords)
    if node.GetMotherVolume() or False:
        return getGlobalLocation(node.GetMotherVolume().GetNode(0))
        # pass
    else:
        return parentCoords



# https://root-forum.cern.ch/t/conversion-from-geant4-to-tgeo-classes-with-vgm/17316  ???? LL

def processNodePhiCut(node,path):
    myStr = ""
    if not node:
        return 0

    nodeName = node.GetName()
    path += f"/{nodeName}"

    volume = node.GetVolume()
    if volume:
        shape = volume.GetShape()
        if shape:
            parentCoords=array('d', [-1,-1,-1])
            g.cd(path)
            trans = g.GetCurrentMatrix()
            globalCoords=array('d', [-1,-1,-1])
            trans.LocalToMaster(shape.GetOrigin(),globalCoords)
            tv2 = ROOT.TVector2(globalCoords[0],globalCoords[1])
            tmpphi = tv2.Phi()
            if not (phimin<tmpphi<phimax):
                print(f"removing {nodeName} with phi={tmpphi}")
                volume.ClearNodes()
    if node.GetNodes():
        for jnode in list(node.GetNodes()):
            if jnode:
                processNodePhiCut(jnode,path)

def recurseThroughDaughterNodesAndRename(node, prefix="Ignore", filterOutNames=["supp", "Cable"]):
    for idau in range(node.GetNdaughters()):
        tmpkid = node.GetDaughter(idau)
        recurseThroughDaughterNodesAndRename(tmpkid, prefix, filterOutNames)

        if not prefix in node.GetName():
            node.SetName(prefix + "_"+node.GetName())
        print(node.GetName())

        # node.SetName(prefix)
        # node.GetVolume().ClearNodes()

    if not node.IsVisible():
        node.SetName("Ignore")

    if any([x in node.GetName() for x in filterOutNames]):
        node.GetVolume().ClearNodes()


processNodePhiCut(g.GetTopNode(),"")

for i,thing in enumerate(list(vol.GetNodes())):
    print(thing.GetName())

    for subsystem in [
        "Vertex",
        "InnerTrackers",
        "OuterTrackers",
        "Solenoid",
        "ECalBarrel",
        "ECalEndcap",
        "HCalBarrel",
        "HCalEndcaps",
        "YokeBarrel",
        "YokeEndcap",
    ]:
        if subsystem in thing.GetName():
            recurseThroughDaughterNodesAndRename(thing,subsystem)


g.Write()
outputFile.Write()

outputFile.ls()
