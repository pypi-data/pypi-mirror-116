def nianuitest():
    try:
        import urwid,os,nian,time
    except:
        print('尝试安装缺失(基于Ubuntu)')
        os.system('pip3 install urwid;su;apt install mpg123 -y')
        print('请重新尝试，或反馈')
    if os.system('mpg123')!=0:
        os.system('su;apt install mpg123')
        print('如无法使用请查看系统，或反馈')
    def menu_button(caption, callback):
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, None, focus_map='reversed')
    
    def sub_menu(caption, choices):
        contents = menu(caption, choices)
        def open_menu(button):
            return top.open_box(contents)
        return menu_button([caption, u'...'], open_menu)
    
    def menu(title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        body.extend(choices)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))
    
    def item_chosen(button):
        response = urwid.Text([u'You chose ', button.label, u'\n'])
        done = menu_button(u'Ok', exit_program)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))
    
    def exit_program(button):
        raise urwid.ExitMainLoop()
    def sta(name):
        global i
        print('\n\n\n')
        os.system(f'wget -q "{nian.nian.kg(name,0,True)[0]}" -O ".nian.mp3"')
        sh=f'nohup mpg123 .nian.mp3 &'
        os.system(sh)
        #print(sh)
        #print(sh.read(),'\n')
        print('执行播放\r')
        sh=os.popen('ps -aux|grep "mpg123 .n"')
        a=0
        for i in sh.read().split(' '):
            if len(i)>1:
                a+=1
            if a==2:
                break
        sh.close()
        print('删除日志缓存\n此输出仅用于观看，可忽略不影响使用')
        os.system('rm nohup.out')
    
    def sto(buttion):
        try:
            a=os.system(f'kill {i}')
        except:
            a=1
        if a==0:
            print('\n\n\n停止播放！')
            rm('')
        else:
            print('\n\n\n失败？请反馈？')
            rm('')
    def rm(buttion):
        os.system('rm .nian.mp3')
        print('\n\n\n删除缓存完成！')
    sou=urwid.Edit(u"音乐名称: \n")
    echo=menu_top = menu(u'初慕苏流年 v-0.0.1', [
        sub_menu(u'音乐🎶聚合', [
            sub_menu(u'音乐搜索',[
            sou
            ]),
            
            sub_menu(u'排行榜', [
                menu_button(u'Text Editor', item_chosen),
                menu_button(u'Terminal', item_chosen),
            ]),
            menu_button(u'停止播放并删除缓存(1-5MB)',sto),
        ]),
        
        
    ])
    class CascadingBoxes(urwid.WidgetPlaceholder):
        max_box_levels = 4
        def __init__(self, box):
            super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
            self.box_level = 0
            self.open_box(box)
    
        def open_box(self, box):
            self.original_widget = urwid.Overlay(urwid.LineBox(box),
                self.original_widget,
                align='center', width=('relative', 80),
                valign='middle', height=('relative', 80),
                min_width=24, min_height=8,
                left=self.box_level * 3,
                right=(self.max_box_levels - self.box_level - 1) * 3,
                top=self.box_level * 2,
                bottom=(self.max_box_levels - self.box_level - 1) * 2)
            self.box_level += 1
    
        def keypress(self, size, key):
            global sou
            if key == 'esc' and self.box_level > 1:
                self.original_widget = self.original_widget[0]
                self.box_level -= 1
            elif key=='q':
                raise urwid.ExitMainLoop()
            elif key=='p':
                print(echo)
                
            elif key=='enter' and len(sou.edit_text)>0:
                sta(sou.edit_text)
                self.original_widget = self.original_widget[0]
                self.box_level -= 1
                sou.edit_text=''
            else:
                return super(CascadingBoxes, self).keypress(size, key)
    top = CascadingBoxes(menu_top)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
    