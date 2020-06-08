# -*- coding: utf-8 -*-
import wx
import wx.xrc


class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title, s_name, p_number):
        wx.Dialog.__init__(self, parent, id, title, size=(1200, 700))

        text = wx.StaticText(self, -1, '스토어팜 소비자 반응 워드클라우드 && 단어 빈도 차트', (20, 20))
        text.SetFont( wx.Font( 26, 72, 90, 90, False, "HY수평선M" ) )

        panel = wx.Panel(self, -1, (20, 150), (550, 400),  style=wx.SUNKEN_BORDER)
        self.picture = wx.StaticBitmap(panel)
        panel.SetBackgroundColour(wx.WHITE)

        panel2 = wx.Panel(self, -1, (600, 150), (550, 400), style=wx.SUNKEN_BORDER)
        self.picture2 = wx.StaticBitmap(panel2)
        panel2.SetBackgroundColour(wx.WHITE)

        #이미지 loads
        self.images = ['image_data/total_wc_{0}_{1}.jpg'.format(s_name, p_number), 'image_data/good_wc_{0}_{1}.jpg'.format(s_name, p_number), 'image_data/moderate_wc_{0}_{1}.jpg'.format(s_name, p_number), 'image_data/bad_wc_{0}_{1}.jpg'.format(s_name, p_number)]
        self.images2 = ['image_data/total_bar_{0}_{1}.jpg'.format(s_name, p_number), 'image_data/good_bar_{0}_{1}.jpg'.format(s_name, p_number), 'image_data/moderate_bar_{0}_{1}.jpg'.format(s_name, p_number), 'image_data/bad_bar_{0}_{1}.jpg'.format(s_name, p_number)]
        authors = ['전체', '만족', '보통', '불만' ]

        wx.ComboBox(self, -1, pos=(20, 80), size=(100, -1), choices=authors, style=wx.CB_READONLY)
        wx.Button(self, 1, 'Close', (1080, 10))
        #----------------------------------------------------------------------화면디자인

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect)


        self.Centre()

    #버튼 클릭 시 이벤트
    def OnClose(self, event):
        self.Close()

    #combobox 클릭 시 이벤트
    def OnSelect(self, event):
        item = event.GetSelection()
        self.picture.SetFocus()
        self.picture.SetBitmap(wx.Bitmap(self.images[item]))
        self.picture2.SetFocus()
        self.picture2.SetBitmap(wx.Bitmap(self.images2[item]))


class MyApp(wx.App):
    # 부모폼 생성자 호출 및 오버라이딩
    def __init__(self, s_name, p_number):
        self.s_name = s_name
        self.p_number = p_number
        wx.App.__init__(self)

    # 화면 호출
    def OnInit(self):
        print(self.s_name, self.p_number)
        dlg = MyDialog(None, -1, '소비자 반응 분석기', self.s_name, self.p_number)
        dlg.ShowModal()
        dlg.Destroy()
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()