from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from boto3.session import Session

from .models import Picture
from .serializers import PictureSerializer
from .pagination import PictureLimitOffsetPagination


def get_s3_data():
    url_list = list()

    session = Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    s3_client = session.client('s3')
    paginator = s3_client.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Prefix='user'
    )

    for page in response_iterator:
        for content in page['Contents']:
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': content['Key']
                }
            )
            url_list.append(url)

    return url_list


class PictureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    pagination_class = PictureLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        #Picture.objects.all().delete()

        if Picture.objects.all().exists() is False:
            Picture.objects.bulk_create(
                [Picture(url=url) for url in get_s3_data()]
            )

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
