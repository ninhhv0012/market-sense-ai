import requests
import os
from celery import shared_task
from django.utils import timezone
from .models import AnalysisRequest
from .scraper import extract_content_from_url

# Lấy URL của AI Service từ biến môi trường
AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL", "http://ai_service:8000")

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 3})
def process_analysis_task(self, request_id):
    """
    Task xử lý chính:
    1. Lấy record từ DB
    2. Cào dữ liệu (Scraping)
    3. Gọi AI Service (LLM)
    4. Lưu kết quả
    """
    try:
        # 1. Lấy record và update status đang xử lý
        analysis_req = AnalysisRequest.objects.get(id=request_id)
        analysis_req.status = AnalysisRequest.ProcessingStatus.PROCESSING
        analysis_req.save()

        # 2. Thực hiện Scraper
        print(f"Starting scraping for: {analysis_req.url}")
        raw_text = extract_content_from_url(analysis_req.url)
        
        # Lưu lại raw text để debug nếu cần
        analysis_req.raw_content = raw_text
        analysis_req.save(update_fields=['raw_content'])

        # 3. Gọi sang AI Microservice (FastAPI)
        print("Calling AI Service...")
        ai_payload = {"text": raw_text[:10000]} # Giới hạn 10k ký tự để tránh lỗi token quá lớn
        response = requests.post(f"{AI_SERVICE_URL}/analyze", json=ai_payload, timeout=60)
        
        response.raise_for_status()
        ai_result = response.json()

        # 4. Lưu kết quả thành công
        analysis_req.result = ai_result
        analysis_req.status = AnalysisRequest.ProcessingStatus.COMPLETED
        analysis_req.updated_at = timezone.now()
        analysis_req.save()
        
        print(f"Task finished successfully for ID: {request_id}")
        return "SUCCESS"

    except AnalysisRequest.DoesNotExist:
        return "REQ_NOT_FOUND"
    
    except Exception as e:
        print(f"Task failed: {str(e)}")
        # Nếu đã retry hết số lần mà vẫn lỗi thì set status FAILED
        if self.request.retries == self.retry_kwargs.get('max_retries'):
            try:
                analysis_req = AnalysisRequest.objects.get(id=request_id)
                analysis_req.status = AnalysisRequest.ProcessingStatus.FAILED
                analysis_req.save()
            except:
                pass
        raise e # Raise để Celery biết là task lỗi và trigger retry