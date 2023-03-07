# p2c_conv
A **VERY WORK IN PROGRESS** command line tool to convert [Portal 2 Puzzle Maker](https://developer.valvesoftware.com/wiki/Portal_2_Puzzle_Maker) data files (.p2c) from v14 (commercial version) to the "old" v12 (educational version). The v12 format is described here: <https://developer.valvesoftware.com/wiki/P2C>.

## Usage
```bash
p2c_conv.py [-h] [-i INPUT] [-o OUTPUT]
```

Or, in some systems, it may be necessary to invoke the python interpreter explicitly:
```bash
python p2c_conv.py [-h] [-i INPUT] [-o OUTPUT]
```

## Building a windows executable

In order to build a windows executable, you may use [PyInstaller](https://pyinstaller.org/):
```bash
pyinstaller p2c_conv.py
```
