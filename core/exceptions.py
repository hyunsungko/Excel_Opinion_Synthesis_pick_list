class OpinionSynthesisError(Exception):
    """기본 커스텀 예외 클래스"""
    pass

class FileValidationError(OpinionSynthesisError):
    """파일 검증 관련 예외"""
    pass

class DataProcessingError(OpinionSynthesisError):
    """데이터 처리 관련 예외"""
    pass
