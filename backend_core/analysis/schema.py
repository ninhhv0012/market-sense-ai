import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar
from .models import AnalysisRequest
from .tasks import process_analysis_task # Import task từ Ticket #4

# 1. Định nghĩa Type (Mapping từ Django Model sang GraphQL Type)
class AnalysisRequestType(DjangoObjectType):
    class Meta:
        model = AnalysisRequest
        fields = ("id", "url", "status", "result", "created_at", "updated_at")
    
    # Định nghĩa tường minh field result là GenericScalar để trả về JSON Object
    # thay vì string. Frontend sẽ nhận được JSON thuần.
    result = GenericScalar()

# 2. Định nghĩa Query (Để Frontend lấy dữ liệu)
class Query(graphene.ObjectType):
    analysis_request = graphene.Field(AnalysisRequestType, id=graphene.UUID(required=True))
    all_analysis_requests = graphene.List(AnalysisRequestType)

    def resolve_analysis_request(root, info, id):
        try:
            return AnalysisRequest.objects.get(id=id)
        except AnalysisRequest.DoesNotExist:
            return None

    def resolve_all_analysis_requests(root, info):
        return AnalysisRequest.objects.all()

# 3. Định nghĩa Mutation (Để Frontend gửi yêu cầu phân tích)
class CreateAnalysis(graphene.Mutation):
    class Arguments:
        url = graphene.String(required=True)

    # Dữ liệu trả về sau khi tạo xong
    analysis_request = graphene.Field(AnalysisRequestType)

    def mutate(root, info, url):
        # Bước 1: Tạo record trong DB với status PENDING
        analysis_request = AnalysisRequest.objects.create(url=url)
        
        # Bước 2: Trigger Celery Task (Async)
        # Đây là điểm kết nối quan trọng: API trả về ngay lập tức,
        # trong khi Worker xử lý ngầm.
        process_analysis_task.delay(analysis_request.id)
        
        # Bước 3: Trả về object vừa tạo cho Frontend
        return CreateAnalysis(analysis_request=analysis_request)

class Mutation(graphene.ObjectType):
    create_analysis = CreateAnalysis.Field()