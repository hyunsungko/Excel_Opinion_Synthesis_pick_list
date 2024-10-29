import ttkbootstrap as tb
from config.settings import THEME_NAME
from ui.main_window import OpinionSynthesisApp
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        root = tb.Window(themename=THEME_NAME)
        app = OpinionSynthesisApp(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"애플리케이션 실행 중 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    main()
