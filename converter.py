import ROOT
import sys

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
f = ROOT.TGeoManager.Import(inputFile)
g = ROOT.TFile.Open(outputFile, "RECREATE")

ROOT.gGeoManager.DefaultColors()
ROOT.gGeoManager.SetPhiRange(phimin=0., phimax=270.)

#print(type(f))
new_phi = f
#new_phi.Edit()
#new_phi.SetPhiRange(phimin=0., phimax=270.)
#print(type(new_phi))
#new_phi.CloseGeometry()
g.WriteObject(new_phi, "default")
