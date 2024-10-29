import ttkbootstrap as tb
from config.settings import (
    ERROR_MESSAGES, UI_TEXTS, UI_STYLES, UI_CONFIG, EXCEL_CONFIG,
    EXCEL_FILETYPES, DEFAULT_FILENAME_FORMAT
)
from ui.components import FileListFrame, ToolTip
from core.data_processor import DataProcessor
from core.exceptions import FileValidationError, DataProcessingError
from utils.logger import get_logger
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

logger = get_logger(__name__)

class OpinionSynthesisApp:
    def __init__(self, root):
        self.root = root
        self.root.title(UI_TEXTS['app_title'])
        self.root.geometry(UI_CONFIG['size'])
        self.data_processor = DataProcessor()
        self.create_widgets()
        
    def create_widgets(self):
        """UI 구성요소 생성"""
        frame = tb.Frame(self.root, padding=UI_STYLES['padding'])
        frame.pack(expand=True, fill='both')

        # 제목
        title_label = tb.Label(
            frame, 
            text=UI_TEXTS['window_title'], 
            font=(UI_CONFIG['font']['family'], UI_CONFIG['font']['title_size'], "bold")
        )
        title_label.pack(pady=20)

        # 파일 선택 버튼
        select_button = tb.Button(
            frame, 
            text=UI_TEXTS['select_button'], 
            command=self.select_files, 
            bootstyle="primary"
        )
        select_button.pack(pady=10)
        ToolTip(select_button, UI_TEXTS['select_tooltip'])

        # 파일 목록
        self.file_listbox = tk.Listbox(
            frame, 
            width=UI_STYLES['listbox_width'], 
            height=UI_STYLES['listbox_height']
        )
        self.file_listbox.pack(pady=10)

        # 생성 버튼
        generate_button = tb.Button(
            frame, 
            text=UI_TEXTS['generate_button'], 
            command=self.generate_summary, 
            bootstyle="success"
        )
        generate_button.pack(pady=10)
        ToolTip(generate_button, UI_TEXTS['generate_tooltip'])

    def select_files(self):
        """파일 선택 다이얼로그"""
        try:
            file_paths = filedialog.askopenfilenames(
                title=UI_TEXTS['file_dialog_title'],
                filetypes=EXCEL_CONFIG['filetypes']
            )
            if file_paths:
                self.file_listbox.delete(0, tk.END)
                for path in file_paths:
                    self.file_listbox.insert(tk.END, path)
                logger.info(f"{len(file_paths)}개의 파일이 선택됨")
        except Exception as e:
            logger.error(f"파일 선택 중 오류 발생: {str(e)}")
            messagebox.showerror(UI_TEXTS['error_title'], f"{ERROR_MESSAGES['file_selection_error'].format(error=str(e))}")

    def generate_summary(self):
        """종합 파일 생성"""
        try:
            selected_files = self.file_listbox.get(0, tk.END)
            
            # 파일 검증
            self.data_processor.validate_files(selected_files)
            
            # 데이터 처리
            final_df = self.data_processor.process_files(selected_files)
            
            # 저장 경로 설정
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = DEFAULT_FILENAME_FORMAT.format(timestamp=timestamp)
            save_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=EXCEL_CONFIG['filetypes'],
                initialfile=default_filename,
                title=UI_TEXTS['save_dialog_title']
            )
            
            if not save_path:
                return
                
            # 파일 저장
            self.data_processor.save_to_excel(final_df, save_path)
            messagebox.showinfo(
                UI_TEXTS['success_title'], 
                UI_TEXTS['save_success'].format(path=save_path)
            )
            
        except (FileValidationError, DataProcessingError) as e:
            messagebox.showerror(UI_TEXTS['error_title'], str(e))
        except Exception as e:
            logger.error(f"예상치 못한 오류 발생: {str(e)}")
            messagebox.showerror(
                UI_TEXTS['error_title'], 
                ERROR_MESSAGES['unexpected_error'].format(error=str(e))
            )
