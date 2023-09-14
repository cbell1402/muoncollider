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
f = ROOT.TFile.Open(inputFile, "READ")    
g = ROOT.TFile.Open(outputFile, "RECREATE")

geo = f.default

g.WriteObject(geo, "New_default")
