from CL.Display.OCCViewer import rgb_color

from CL.lib import Path
import re
from OCC.Core.gp import gp_OX, gp_OZ
from OCC.Core.gp import gp_Ax1, gp_Origin, gp_Dir, gp_Vec, gp_Quaternion
import os

def read_Nc_File(file):
    with open(file) as f:
        ncLines = f.readlines()
    path = []
    GCode = 0
    block = 1
    has_BLOCK_END = False
    ID = 0
    error_txt = ''
    try:
        for i in ncLines:
            error_txt = i
            ncLine = Path.Path()
            ncLine.OriginText = i
            if "BEAMON" in i or "M60" in i:
                GCode = 1
            if "BEAMOFF" in i or "M61" in i:
                GCode = 0
            if i[0] == "N":
                n = i.split()[0]
                n = n.split("N")[1]
                ncLine.N = n
            if "START of" in i:
                n = i.split(".")[1]
                n = n.split(")")[0]
                if not has_BLOCK_END:
                    block = int(n)
            if "END of" in i:
                block += 1
                has_BLOCK_END = True
            if "G00 X" in i or "G01 X" in i:
                if 'X' in i:
                    ncLine.X = float(i.split('X')[1].split()[0])
                if 'Y' in i:
                    ncLine.Y = float(i.split('Y')[1].split()[0])
                if 'Z' in i:
                    ncLine.Z = float(i.split('Z')[1].split()[0])
                if 'A' in i:
                    ncLine.A = float(i.split('A')[1].split()[0])
                if 'C' in i:
                    ncLine.C = float(i.split('C')[1].split()[0])
                if 'F' in i:
                    ncLine.F = float(i.split('F')[1].split()[0])
                ncLine.GType = GCode
                ncLine.BlockNum = block
                ncLine.Line = True

            ncLine.BlockNum = block

            ncLine.ID = ID
            ID += 1
            path.append(ncLine)
        # =========================
        return path
    except:
        raise BaseException(error_txt)




def update_Nc_List(paths):
    new_text_lsit = []
    preblock = None
    for block in paths:
        if block.Line:
            text = block.OriginText
            if block.IsSameAsPrePoint:
                text = re.sub(r'X[-]*\d*.\d*', 'X{}'.format(round(preblock_withX.X, 3)), text)
                text = re.sub(r'Y[-]*\d*.\d*', 'Y{}'.format(round(preblock_withX.Y, 3)), text)
                text = re.sub(r'Z[-]*\d*.\d*', 'Z{}'.format(round(preblock_withX.Z, 3)), text)
                text = re.sub(r'A[-]*\d*.\d*', 'A{}'.format(round(preblock_withX.A, 3)), text)
                text = re.sub(r'C[-]*\d*.\d*', 'C{}'.format(round(preblock_withX.C, 3)), text)
            else:
                text = re.sub(r'X[-]*\d*.\d*', 'X{}'.format(round(block.X, 3)), text)
                text = re.sub(r'Y[-]*\d*.\d*', 'Y{}'.format(round(block.Y, 3)), text)
                if block.Z:
                    text = re.sub(r'Z[-]*\d*.\d*', 'Z{}'.format(round(block.Z, 3)), text)
                text = re.sub(r'A[-]*\d*.\d*', 'A{}'.format(round(block.A, 3)), text)
                text = re.sub(r'C[-]*\d*.\d*', 'C{}'.format(round(block.C, 3)), text)
            block.EditedText = text
            new_text_lsit.append(text)
        else:
            new_text_lsit.append(block.OriginText)
        preblock = block
        if block.X is not None:
            preblock_withX = block
    return new_text_lsit


# 文件打开时，显示的后缀过滤器
NC_FILE_FORMAT = 'Beckhoff NC File(*.nc)'
# 处理nc文件函数
READ_NC_FILE = read_Nc_File
# 更新NC文件
UPDATE_NC_LIST = update_Nc_List
# A轴旋转点Z值高度
A_CENTER_Z = 278.398
# 喷嘴高度
HEAD_HEIGHT = 6.0

A_AIX1 = gp_Ax1(gp_Origin(), gp_Dir(-1., 0., 0.))
C_AIX1 = gp_Ax1(gp_Origin(), gp_Dir(0., 0., -1.))


A_MODEL = os.path.join(os.path.dirname(__file__), 'head.brep')
# C_MODEL = os.path.join(os.path.dirname(__file__), 'dazu_c.brep')
C_MODEL = ''
A_NAME = 'A'
C_NAME = 'C'

COLOR = rgb_color(0.55, 0.55, 0.55)
