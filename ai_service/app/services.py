import os
import json
from openai import AsyncOpenAI
from fastapi import HTTPException
from .schemas import AnalysisResult

# Khởi tạo client OpenAI (Async để không block request)
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def analyze_text_with_llm(text: str) -> dict:
    # 1. Prompt Engineering: Kỹ thuật Persona + Explicit Constraints
    system_prompt = """
    You are a Senior Market Research Analyst. Your job is to extract insights from technical articles.
    
    Output must be a valid JSON object matching this schema:
    {
        "summary": "Short summary...",
        "sentiment": "Positive/Negative/Neutral",
        "key_entities": ["Entity1", "Entity2"],
        "swot": {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": []
        }
    }
    """

    try:
        # 2. Gọi OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o", # Hoặc gpt-4o nếu bạn có budget, bản turbo-0125 tối ưu cho JSON
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze the following text:\n\n{text[:4000]}"} # Cắt text nếu quá dài để tiết kiệm token
            ],
            response_format={"type": "json_object"}, # KEY FEATURE: Bắt buộc trả về JSON
            temperature=0.3, # Giảm sáng tạo để tăng tính chính xác
        )

        # 3. Parse và Validate kết quả
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # Dùng Pydantic để validate lần cuối (Double check)
        validated_data = AnalysisResult(**data)
        
        return validated_data.model_dump()

    except Exception as e:
        print(f"AI Service Error: {str(e)}")
        # Trong thực tế nên log vào Sentry/Datadog
        raise HTTPException(status_code=500, detail=f"LLM Processing Failed: {str(e)}")