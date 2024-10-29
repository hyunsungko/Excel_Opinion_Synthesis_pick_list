import tkinter as tk
import ttkbootstrap as tb
from config.settings import FONT_FAMILY, TOOLTIP_FONT_SIZE, UI_CONFIG, UI_STYLES

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        
    def show_tip(self, event=None):
        """툴팁 표시"""
        if self.tipwindow or not self.text:
            return
            
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tb.Label(
            tw, 
            text=self.text, 
            justify='left',
            background=UI_STYLES['tooltip_bg'], 
            relief=UI_STYLES['tooltip_relief'], 
            borderwidth=UI_STYLES['tooltip_borderwidth'],
            font=(UI_CONFIG['font']['family'], UI_CONFIG['font']['tooltip_size'])
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        """툴팁 숨기기"""
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class FileListFrame(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        
    def create_widgets(self):
        """파일 목록 위젯 생성"""
        self.listbox = tk.Listbox(
            self, 
            width=UI_STYLES['listbox_width'], 
            height=UI_STYLES['listbox_height']
        )
        self.listbox.pack(pady=10)
        
    def get_files(self):
        """선택된 파일 목록 반환"""
        return self.listbox.get(0, tk.END)
        
    def set_files(self, file_paths):
        """파일 목록 설정"""
        self.listbox.delete(0, tk.END)
        for path in file_paths:
            self.listbox.insert(tk.END, path)
