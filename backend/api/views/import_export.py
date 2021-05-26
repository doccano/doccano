from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class Features(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({
            'cloud_upload': bool(settings.CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER),
        })


# class CloudUploadAPI(APIView):
#     permission_classes = TextUploadAPI.permission_classes
#
#     def get(self, request, *args, **kwargs):
#         try:
#             project_id = request.query_params['project_id']
#             file_format = request.query_params['upload_format']
#             cloud_container = request.query_params['container']
#             cloud_object = request.query_params['object']
#         except KeyError as ex:
#             raise ValidationError('query parameter {} is missing'.format(ex))
#
#         try:
#             cloud_file = self.get_cloud_object_as_io(cloud_container, cloud_object)
#         except ContainerDoesNotExistError:
#             raise ValidationError('cloud container {} does not exist'.format(cloud_container))
#         except ObjectDoesNotExistError:
#             raise ValidationError('cloud object {} does not exist'.format(cloud_object))
#
#         TextUploadAPI.save_file(
#             user=request.user,
#             file=cloud_file,
#             file_format=file_format,
#             project_id=project_id,
#         )
#
#         next_url = request.query_params.get('next')
#
#         if next_url == 'about:blank':
#             return Response(data='', content_type='text/plain', status=status.HTTP_201_CREATED)
#
#         if next_url:
#             return redirect(next_url)
#
#         return Response(status=status.HTTP_201_CREATED)
#
#     @classmethod
#     def get_cloud_object_as_io(cls, container_name, object_name):
#         provider = settings.CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER.lower()
#         account = settings.CLOUD_BROWSER_APACHE_LIBCLOUD_ACCOUNT
#         key = settings.CLOUD_BROWSER_APACHE_LIBCLOUD_SECRET_KEY
#
#         driver = get_driver(DriverType.STORAGE, provider)
#         client = driver(account, key)
#
#         cloud_container = client.get_container(container_name)
#         cloud_object = cloud_container.get_object(object_name)
#
#         return iterable_to_io(cloud_object.as_stream())
