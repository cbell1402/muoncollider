import ROOT
import sys
import shutil

try:
    input = raw_input
except:
    pass

if len(sys.argv) < 3:
    print("Usage: converter.py input_file output_file")
    sys.exit(1)

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
ROOT.gGeoManager.SetPhiRange(phimin=0., phimax=270.)
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

def recurseThroughDaughterNodesAndRename(node, newName = "IgnoreMe", editName=False):
    for idau in range(node.GetNdaughters()):
        tmpkid = node.GetDaughter(idau)
        recurseThroughDaughterNodesAndRename(tmpkid, newName, editName)
    if editName:
        node.SetName(newName + "_"+node.GetName())
    else:
        node.SetName(newName)
    node.GetVolume().Clear()


for i,thing in enumerate(list(vol.GetNodes())):
    print(thing.GetName())
    if "Vertex_6" in thing.GetName():
        recurseThroughDaughterNodesAndRename(thing,"Vertex",True)



g.Write()
outputFile.Write()

# # print(g.GetListOfNodes())
# for i,thing in enumerate(list(g.GetListOfVolumes()) ):
#     print(thing.GetName())
#     # thing.Delete()
#     if i==0:
#         print(dir(thing))
#         break
#     pass


# g.Dump()

# def processNode(tmpnode):

#     tmpName = f.GetCurrentNode().GetName()
#     print(tmpName)
#     print(f.GetCurrentNode().Dump())

#     # Do some checks and change stuff.
#     # Now I'm done with this node. Let's see what's next.

#     # Check if there are any siblings.
#     f.CdNext()
#     if tmpName!=f.GetCurrentNode().GetName():
#         # I found a new node to look at. Let's do it.
#         pass
#     else:
#         print("blah")
#         # This layer is exhausted. Time to move down.
#         try:
#             f.CdDown(6)
#             processNode(f.GetCurrentNode())
#         except:
#             print("caused exception")
#         # for i in range(100):
#         #     try:
#         #         f.CdDown(i)
#         #         # found a down. process it.
#         #         f.CdUp()
#         #     except:
#         #         break


# Starting from the top

outputFile.ls()

# f.CdTop()
# processNode(f.GetCurrentNode())



# try:
#     f.CdNext()
# except:




# # new_phi.Edit()
# new_phi.SetPhiRange(phimin=0., phimax=270.)
# print(new_phi.GetGDMLMatrix())
# #print(type(new_phi))
# #new_phi.CloseGeometry()
# g.WriteObject(new_phi, "default")
