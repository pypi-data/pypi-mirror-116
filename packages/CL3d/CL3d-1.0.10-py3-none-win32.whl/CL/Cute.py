from CL import config
from CL.Display.SimpleGui import init_display
from CL.process import initGui
from CL.lib.Base import Display as Dis
from CL.lib.Menu import initMenu
from CL.res.dark_blue_qss import qss


def init(par_win=None):
    display, start_display, get_Viewer3d, add_function_to_menu = init_display(par_win=par_win)
    initMenu(get_Viewer3d, add_function_to_menu)
    Dis.display = display
    Dis.CDisplay = display.Context.Display
    Dis.CUpdate = display.Context.UpdateCurrentViewer
    Dis.C = display.Context
    Dis.Win = get_Viewer3d()
    Dis.Drawer = display.Context.DefaultDrawer()
    Viewer3d_Win = get_Viewer3d()
    init = initGui.InitGui(Viewer3d_Win)
    Viewer3d_Win.setStyleSheet(qss)
    Dis.mainWin = init.initMainGui()

    def start():
        start_display()


    Viewer3d_Win.start = start
    Viewer3d_Win.action = Dis.mainWin
    return Viewer3d_Win

# w = init()
# w.start()
# f_path = w.action.ft.OpenFile()
