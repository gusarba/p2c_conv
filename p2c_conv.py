#!/usr/bin/env python3

from shlex import shlex
import pprint


def DictFromBracket(lex):
    root = dict()

    # Next token is key or }
    key = lex.get_token()
    key = key.strip('"')
    while key != "}":
        #print("KEY:", key)
        if key not in root.keys():
            root[key] = []
        # Next token is value or {
        val = lex.get_token()
        val = val.strip('"')
        if val == "{":
            root[key] += [DictFromBracket(lex)]
        else:
            #print("VALUE:", val)
            root[key] += [val]
        key = lex.get_token()
        key = key.strip('"')

    for k, v in root.items():
        if len(v) == 1:
            root[k] = v[0]

    return root

def FillVoxelKey(root, voxels, key):
    solid = root["portal2_puzzle"]["Voxels"][key]
    for zz, v in solid.items():
        iz = int(zz[1:])
        for yy, vv in v.items():
            iy = int(yy[1:])
            ix = 0
            for char in vv:
                #print(key, str(ix), str(iy), str(iz))
                # Ignore "f"
                if char != "f":
                    voxels[ix][iy][iz][key] = char
                    ix = ix + 1

def List2p2c(key, lis, deep):
    t = "\t" * deep
    out = ""
    for item in lis:
        #out += t + '"' + key + '"' + ' '
        out += Dict2p2c(key, item, deep)
    return out


def Dict2p2c(key, root, deep=0):
    t = "\t" * deep

    out = "\n" + t + '"' + str(key) + '"' + '\n' + t + '{\n'
    t = "\t" * (deep + 1)
    for k, v in root.items():
        if isinstance(v, dict):
            #out += t + '"' + k + '"' + ' '
            out += Dict2p2c(k, v, deep+1)
        elif isinstance(v, list):
            out += List2p2c(k, v, deep+1)
        else:
            out += t + '"' + k + '"' + ' '
            out += '"' + str(v) + '"' + '\n'
    t = "\t" * deep
    out += t + "}\n"
    return out
    
def VoxelsList2Dict(voxels):
    d = dict()
    d["Voxel"] = []

    # Dump voxels 3-dimensional list into a plain list
    for lx in voxels:
        for ly in lx:
            for lz in ly:
                d["Voxel"].append(lz)

    return d



def main():
    """
    Read Portal 2 v14 P2C file and write a v12 P2C compatible file
    """
    import sys
    import argparse

    parser = argparse.ArgumentParser(prog='p2c_conv', description=main.__doc__)
    parser.add_argument('-i', '--input',
                        default=sys.stdin,
                        type=argparse.FileType('r'),
                        help='input p2c file (stdin if not specified)')
    parser.add_argument('-o', '--output',
                        default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='output p2c file (stdout if not specified)')

    args = parser.parse_args()

    
    root = dict()
    #args.input.seek(0, 0)

    # Setup tokenizer
    lex = shlex(args.input)
    tok = lex.get_token()

    # Remove double-quotes
    tok = tok.replace('"', '')
    bracket = lex.get_token()
    # TODO: Check portal2_puzzle string and bracket
    root[tok] = DictFromBracket(lex)

    #pprint.pprint(root)

    # ChamberSize
    chamber_size = root["portal2_puzzle"]["ChamberSize"]
    x, y, z = chamber_size.split()
    x = int(x)
    y = int(y)
    z = int(z)

    print("Chamber dimensions are: " + str(x) + "x" + str(y) + "x" + str(z))

    # Version
    if root["portal2_puzzle"]["Version"] != "12":
        print("Puzzle version is " + str(root["portal2_puzzle"]["Version"] + ". Changing to 12"))
        root["portal2_puzzle"]["Version"] = 12
    if "Coop" in root["portal2_puzzle"].keys():
        del root["portal2_puzzle"]["Coop"]

    # Build voxel map
    voxels = []
    for ix in range(x+1):
        l = []
        for iy in range(y+1):
            ll = []
            for iz in range(z+1):
                d = dict()
                d["Position"] = str(ix) + " " + str(iy) + " " + str(iz)
                d["Solid"] = "1"
                d["Portal0"] = "1"
                d["Portal1"] = "1"
                d["Portal2"] = "1"
                ll.append(d)
            l.append(ll)
        voxels.append(l)
    #pprint.pprint(voxels)

    # Turn v14 info into v12 info
    FillVoxelKey(root, voxels, "Solid")
    FillVoxelKey(root, voxels, "Portal0")
    FillVoxelKey(root, voxels, "Portal1")
    FillVoxelKey(root, voxels, "Portal2")
    #pprint.pprint(voxels)

    # Dump info back into v12 P2C format
    del root["portal2_puzzle"]["Voxels"]
    root["portal2_puzzle"]["Voxels"] = VoxelsList2Dict(voxels)
    out = Dict2p2c("portal2_puzzle", root["portal2_puzzle"], 0)
    #print(out)
    args.output.write(out)
    

if __name__ == '__main__':
    main()

