import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class AnalysisRequest(models.Model):
    # Sử dụng TextChoices cho Status - Clean code pattern trong Django mới
    class ProcessingStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')

    # Dùng UUID làm Primary Key để bảo mật (không lộ số lượng record) và dễ scale
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    url = models.URLField(max_length=500, help_text="URL bài viết cần phân tích")
    
    # Enum status field
    status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.PENDING,
        db_index=True # Indexing để query status nhanh hơn
    )
    
    # Lưu nội dung thô cào từ web (có thể rất dài nên dùng TextField)
    raw_content = models.TextField(blank=True, null=True)
    
    # KEY FEATURE: JSONField
    # Postgres lưu cái này dưới dạng binary JSON (JSONB), cho phép query cực nhanh
    # Ví dụ: AnalysisRequest.objects.filter(result__sentiment='positive')
    result = models.JSONField(blank=True, null=True, help_text="Kết quả phân tích từ AI")
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Analysis Request"
        verbose_name_plural = "Analysis Requests"

    def __str__(self):
        return f"{self.url} - {self.status}"