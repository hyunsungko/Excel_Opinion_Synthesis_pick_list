import pandas as pd
from datetime import datetime
from typing import List, Set, Dict, Optional
from config.settings import (
    DICT_OPINION_KEY,
    DICT_SELECTION_KEY,
    REQUIRED_COLUMNS, 
    COLUMN_REVIEWER, 
    COLUMN_CODE, 
    COLUMN_SELECTION, 
    COLUMN_OPINION,
    FIXED_COLUMNS_TO_REMOVE,
    OPINION_PREFIX,
    EMPTY_OPINION,
    CODE_COLUMN
)
from core.exceptions import FileValidationError, DataProcessingError
from utils.logger import get_logger

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self):
        self.reviewers: Set[str] = set()
        self.first_df: Optional[pd.DataFrame] = None
        
    def validate_files(self, file_paths: List[str]) -> None:
        """파일 유효성 검증"""
        if not file_paths:
            raise FileValidationError("종합할 엑셀 파일을 선택하세요.")
            
        for file in file_paths:
            df = pd.read_excel(file)
            if not all(col in df.columns for col in REQUIRED_COLUMNS):
                raise FileValidationError(f"파일 {file}에 필요한 열이 없습니다.\n필요한 열: {', '.join(REQUIRED_COLUMNS)}")

    def process_files(self, file_paths: List[str]) -> pd.DataFrame:
        """파일 처리 및 데이터 종합"""
        try:
            logger.info("파일 처리 시작")
            df_list = []
            
            for file in file_paths:
                df = pd.read_excel(file)
                if self.first_df is None:
                    self.first_df = df
                    
                df_list.append(df)
                self.reviewers.update(df[COLUMN_REVIEWER].dropna().unique())
            
            if not self.reviewers:
                raise DataProcessingError("선택된 파일에서 검토자를 찾을 수 없습니다.")
                
            self.reviewers = sorted(self.reviewers)
            return self._merge_data(df_list)
            
        except Exception as e:
            logger.error(f"데이터 처리 중 오류 발생: {str(e)}")
            raise DataProcessingError(f"데이터 처리 중 오류가 발생했습니다: {str(e)}")

    def _merge_data(self, df_list: List[pd.DataFrame]) -> pd.DataFrame:
        """데이터 병합 로직"""
        try:
            # 고정값 열 설정
            fixed_columns = self.first_df.columns.tolist()
            for col in FIXED_COLUMNS_TO_REMOVE:
                fixed_columns.remove(col)

            # 최종 데이터프레임 초기화
            final_df = self.first_df[fixed_columns].copy()
            final_df = final_df.drop_duplicates(subset=[CODE_COLUMN])
            final_df[COLUMN_OPINION] = EMPTY_OPINION
            
            # 검토자별 선정여부 열 추가
            for reviewer in self.reviewers:
                final_df[reviewer] = EMPTY_OPINION

            # 데이터 종합을 위한 딕셔너리 생성
            summary_dict = self._create_summary_dict(df_list)
            
            # 최종 데이터 입력
            self._fill_final_dataframe(final_df, summary_dict)
            
            # 열 순서 재정렬
            column_order = [CODE_COLUMN] + [col for col in fixed_columns if col != CODE_COLUMN] + [COLUMN_OPINION] + list(self.reviewers)
            final_df = final_df[column_order]
            
            logger.info("데이터 병합 완료")
            return final_df
            
        except Exception as e:
            logger.error(f"데이터 병합 중 오류 발생: {str(e)}")
            raise DataProcessingError(f"데이터 병합 중 오류가 발생했습니다: {str(e)}")

    def _create_summary_dict(self, df_list: List[pd.DataFrame]) -> Dict:
        """검토 데이터 종합 딕셔너리 생성"""
        summary_dict = {}
        
        for df in df_list:
            for _, row in df.iterrows():
                code = row[COLUMN_CODE]
                reviewer = row[COLUMN_REVIEWER]  # '검토자' 대신 상수 사용
                selection = row[COLUMN_SELECTION]
                opinion = row[COLUMN_OPINION]
                
                if pd.isna(code) or pd.isna(reviewer):
                    continue

                if code not in summary_dict:
                    summary_dict[code] = {}

                if reviewer not in summary_dict[code]:
                    summary_dict[code][reviewer] = {
                        DICT_SELECTION_KEY: selection if pd.notna(selection) else EMPTY_OPINION,
                        DICT_OPINION_KEY: []
                    }

                if pd.notna(opinion):
                    summary_dict[code][reviewer][DICT_OPINION_KEY].append(opinion)
                    
        return summary_dict

    def _fill_final_dataframe(self, final_df: pd.DataFrame, summary_dict: Dict) -> None:
        """최종 데이터프레임에 데이터 입력"""
        for code in final_df[CODE_COLUMN]:
            if code in summary_dict:
                # 각 검토자의 선정여부 입력
                for reviewer in self.reviewers:
                    if reviewer in summary_dict[code]:
                        selection = summary_dict[code][reviewer][DICT_SELECTION_KEY]
                        final_df.loc[final_df[CODE_COLUMN] == code, reviewer] = selection

                # 검토의견 종합
                opinions = []
                for reviewer in self.reviewers:
                    if reviewer in summary_dict[code]:
                        reviewer_opinions = summary_dict[code][reviewer][DICT_OPINION_KEY]
                        if reviewer_opinions:
                            for op in reviewer_opinions:
                                opinions.append(f"{OPINION_PREFIX}{reviewer}: {op}")
                
                if opinions:
                    final_df.loc[final_df[CODE_COLUMN] == code, COLUMN_OPINION] = "\n".join(opinions)

    def save_to_excel(self, df: pd.DataFrame, save_path: str) -> None:
        """엑셀 파일 저장"""
        try:
            df.to_excel(save_path, index=False)
            logger.info(f"파일 저장 완료: {save_path}")
        except Exception as e:
            logger.error(f"파일 저장 중 오류 발생: {str(e)}")
            raise DataProcessingError(f"파일 저장 중 오류가 발생했습니다: {str(e)}")
