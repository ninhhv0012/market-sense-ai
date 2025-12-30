from typing import List, Optional
from pydantic import BaseModel, Field

# Định nghĩa cấu trúc SWOT
class SWOT(BaseModel):
    strengths: List[str] = Field(..., description="Điểm mạnh tìm thấy trong bài viết")
    weaknesses: List[str] = Field(..., description="Điểm yếu hoặc hạn chế")
    opportunities: List[str] = Field(..., description="Cơ hội thị trường hoặc tiềm năng")
    threats: List[str] = Field(..., description="Rủi ro hoặc thách thức")

# Định nghĩa cấu trúc kết quả trả về cuối cùng
class AnalysisResult(BaseModel):
    summary: str = Field(..., description="Tóm tắt ngắn gọn nội dung (dưới 100 từ)")
    sentiment: str = Field(..., description="Cảm xúc chung: Positive, Negative, hoặc Neutral")
    key_entities: List[str] = Field(..., description="Các công ty, công nghệ hoặc nhân vật chính được nhắc đến")
    swot: SWOT

# Định nghĩa Request Body
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Nội dung văn bản cần phân tích")