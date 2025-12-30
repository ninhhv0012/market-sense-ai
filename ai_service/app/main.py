from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from .schemas import AnalyzeRequest, AnalysisResult
from .services import analyze_text_with_llm

app = FastAPI(
    title="MarketSense AI Microservice",
    description="Service chuyên biệt xử lý phân tích thị trường bằng LLM",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "ai_service"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_market_text(request: AnalyzeRequest):
    """
    Endpoint nhận văn bản thô và trả về phân tích SWOT + Sentiment.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = await analyze_text_with_llm(request.text)
    return result