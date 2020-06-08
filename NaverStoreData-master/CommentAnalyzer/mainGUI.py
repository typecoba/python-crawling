# -*- coding: utf-8 -*-

import wx
import wx.xrc
import sqlite3
import crawlingFinal
import nounExtract



class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='네이버 스토어팜 소비자 반응 분석기', pos=wx.DefaultPosition,
                          size=wx.Size(1300, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel4 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText10 = wx.StaticText(self.m_panel4, wx.ID_ANY, u"URL :", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        bSizer15.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.txtUrl = wx.TextCtrl(self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.txtUrl, 1, wx.ALL, 5)

        self.btnView = wx.Button(self.m_panel4, wx.ID_ANY, u"확인", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.btnView, 0, wx.ALL, 5)

        self.m_panel4.SetSizer(bSizer15)
        self.m_panel4.Layout()
        bSizer15.Fit(self.m_panel4)
        bSizer14.Add(self.m_panel4, 0, wx.EXPAND | wx.ALL, 5)

        self.m_panel6 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        self.lstList = wx.ListCtrl(self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.VSCROLL)
        bSizer18.Add(self.lstList, 1, wx.ALL|wx.EXPAND, 5)

        self.m_panel6.SetSizer(bSizer18)
        self.m_panel6.Layout()
        bSizer18.Fit(self.m_panel6)
        bSizer14.Add(self.m_panel6, 1, wx.EXPAND | wx.ALL, 5)


        self.SetSizer(bSizer14)
        self.Layout()
        #---------------------------------------------------화면 디자인
        #초기 ListCtrl 컬럼명 설정
        self.lstList.InsertColumn(0, 'index', width=50)
        self.lstList.InsertColumn(1, 'type', width=100)
        self.lstList.InsertColumn(2, 'prefer', width=50)
        self.lstList.InsertColumn(3, 'content', width=850)
        self.lstList.InsertColumn(4, 'date', width=200)

        self.Centre(wx.BOTH)

        # Connect Events
        self.btnView.Bind(wx.EVT_BUTTON, self.View)
        self.txtUrl.SetFocus()

    # Button 클릭 이벤트 설정
    def View(self, event):
        self.lstList.ClearAll()
        self.lstList.InsertColumn(0, 'index', width=50)
        self.lstList.InsertColumn(1, 'type', width=100)
        self.lstList.InsertColumn(2, 'prefer', width=50)
        self.lstList.InsertColumn(3, 'content', width=850)
        self.lstList.InsertColumn(4, 'date', width=200)

        #TextCtrl 값 추출
        url = str(self.txtUrl.GetValue())
        #TextCtrl 값을 인자로 하여crawlingFinal.main() 함수 실행
        data = crawlingFinal.main(url)
        data

        #return으로 받은 상품명과 제품번호에 해당하는 DB table select
        conn = sqlite3.connect('naverComment.db')
        cur = conn.cursor()
        cur.execute('select * from comment_{0}_{1}'.format(data[0], data[1]))

        #ListCtrl에 table 매핑하여 출력
        for row in cur:
            i = self.lstList.InsertItem(5000, 0)
            self.lstList.SetItem(i, 0, str(row[0]))
            self.lstList.SetItem(i, 1, str(row[1]))
            self.lstList.SetItem(i, 2, str(row[2]))
            self.lstList.SetItem(i, 3, str(row[3]))
            self.lstList.SetItem(i, 4, str(row[4]))
        cur.close()
        conn.close()

        #MessageDialog를 통해 텍스트 마이닝 수행
        dlg = wx.MessageDialog(self, '텍스트 분석을 하시겠습니까?', '텍스트 분석', wx.YES_NO)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            wx.MessageBox('분석 중입니다.','형태소 분석', wx.OK)
            # 명사추출과 워드클라우드 실행
            nounExtract.main(data[0],data[1])
            import createChart
            createChart.main(data[0], data[1])
            box = wx.MessageBox("형태소 분석이 완료 되었습니다.\n '예(Y)'를 클릭하시면 그래프를 확인하실 수 있습니다.", '형태소 분석',wx.OK)
            #MessageBox의 '예'를 클릭하면 chartGUI에 제품명과 제품번호를 return하고 객체생성
            if box == wx.OK:
                from chartGUI import MyApp
                s_name = data[0]
                p_number = data[1]
                app = MyApp(s_name = s_name, p_number = p_number)
                app.MainLoop()
            dlg.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame1(None).Show()
    app.MainLoop()
