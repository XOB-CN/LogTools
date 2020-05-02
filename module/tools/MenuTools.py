# -*- coding: utf-8 -*-

class AddMenuTools():
    '''
    针对不同的产品, 在 guiMain 上的 Tools 下面增加不同的选项
    '''
    def __init__(self, product_name, guiMain):
        self.procuct_name = product_name
        self.guiMain = guiMain

        # MicroFocus ITOM OBM/OMi
        if self.procuct_name == 'OBM/OMi':
            self.set_mf_itom_obm_menu()

    def set_mf_itom_obm_menu(self):
        menu = self.guiMain.menubar.addMenu('Tools')
        menu_ci_resolver = menu.addAction('CI Resolver')
        menu_rtsm = menu.addAction('RTSM')
        menu_epi = menu.addAction('Event Processing Interface')
        menu_pd = menu.addAction('Performance Dashboard')
        menu_ma = menu.addAction('Monitoring Automation')

        def demo(x=None, y=None, z=None):
            print('demo', x, y, z)

        def demo2(x=None, y=None, z=None):
            print('demo2', x, y, z)

        menu_ci_resolver.triggered.connect(demo)
        menu_rtsm.triggered.connect(demo2)