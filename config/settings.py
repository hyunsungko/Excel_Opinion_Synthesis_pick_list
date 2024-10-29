# 애플리케이션 설정값
APP_TITLE = "의견종합_선정리스트_v2"
WINDOW_SIZE = "600x500"
THEME_NAME = "cosmo"

# UI 관련 설정
FONT_FAMILY = "Noto Sans KR"
TITLE_FONT_SIZE = 20
TOOLTIP_FONT_SIZE = 9

# 필수 엑셀 컬럼
REQUIRED_COLUMNS = ['문항코드', '검토자', '선정여부', '검토의견']

# 파일 관련 설정
EXCEL_FILETYPES = [("Excel files", "*.xlsx *.xls")]
DEFAULT_FILENAME_FORMAT = "선정리스트 종합_{timestamp}.xlsx"

# 컬럼명 상수 (DataFrame에서 사용)
COLUMN_CODE = "문항코드"
COLUMN_REVIEWER = "검토자"
COLUMN_SELECTION = "선정여부"
COLUMN_OPINION = "검토의견"

# 데이터 처리 관련 상수
FIXED_COLUMNS_TO_REMOVE = [COLUMN_REVIEWER, COLUMN_SELECTION, COLUMN_OPINION]
OPINION_PREFIX = "→"
EMPTY_OPINION = ""
CODE_COLUMN = COLUMN_CODE

# 데이터 처리 관련 상수
SELECTION_KEY = "선정여부"
OPINION_KEY = "검토의견"

# 딕셔너리 키값 상수 (summary_dict에서 사용)
DICT_SELECTION_KEY = COLUMN_SELECTION  # "선정여부"
DICT_OPINION_KEY = COLUMN_OPINION     # "검토의견"

# UI 텍스트
UI_TEXTS = {
    'app_title': APP_TITLE,
    'window_title': "의견 종합 선정리스트 생성기",
    'select_button': "엑셀 파일 선택",
    'generate_button': "종합 파일 생성",
    'select_tooltip': "종합할 엑셀 파일들을 선택합니다.",
    'generate_tooltip': "선정리스트 종합 파일을 생성합니다.",
    'file_dialog_title': "엑셀 파일을 선택하세요",
    'save_dialog_title': "저장할 위치와 파일명을 선택하세요",
    'success_message': "종합 파일이 저장되었습니다",
    'error_title': "오류",
    'success_title': "성공",
    'save_success': "종합 파일이 저장되었습니다:\n{path}"
}

# UI 스타일
UI_STYLES = {
    'tooltip_bg': "#ffffe0",
    'tooltip_relief': 'solid',
    'tooltip_borderwidth': 1,
    'padding': 20,
    'listbox_width': 100,
    'listbox_height': 10  # 20에서 10으로 수정
}

# UI 관련 설정
UI_CONFIG = {
    'title': APP_TITLE,
    'size': WINDOW_SIZE,
    'theme': THEME_NAME,
    'font': {
        'family': "Noto Sans KR",
        'title_size': 20,
        'tooltip_size': 9
    }
}

# 엑셀 관련 설정
EXCEL_CONFIG = {
    'required_columns': REQUIRED_COLUMNS,
    'filetypes': [("Excel files", "*.xlsx *.xls")],
    'default_filename': "선정리스트 종합_{timestamp}.xlsx"
}

# 에러 메시지
ERROR_MESSAGES = {
    'no_files': "종합할 엑셀 파일을 선택하세요.",
    'missing_columns': "파일 {file}에 필요한 열이 없습니다.\n필요한 열: {columns}",
    'no_reviewers': "선택된 파일에서 검토자를 찾을 수 없습니다.",
    'processing_error': "데이터 처리 중 오류가 발생했습니다: {error}",
    'save_error': "파일 저장 중 오류가 발생했습니다: {error}",
    'file_selection_error': "파일 선택 중 오류가 발생했습니다: {error}",
    'unexpected_error': "예상치 못한 오류가 발생했습니다: {error}"
}
