import os

from django.conf import settings

from ...models import Role, RoleMapping

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')


def create_default_roles():
    Role.objects.get_or_create(name=settings.ROLE_PROJECT_ADMIN)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATOR)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATION_APPROVER)


def assign_user_to_role(project_member, project, role_name):
    role, _ = Role.objects.get_or_create(name=role_name)
    if RoleMapping.objects.filter(user=project_member, project=project).exists():
        mapping = RoleMapping.objects.get(user=project_member, project=project)
        mapping.role = role
        mapping.save()
    else:
        mapping = RoleMapping.objects.get_or_create(role_id=role.id, user_id=project_member.id, project_id=project.id)
    return mapping


def remove_all_role_mappings():
    RoleMapping.objects.all().delete()


class TestUtilsMixin:
    def _patch_project(self, project, attribute, value):
        old_value = getattr(project, attribute, None)
        setattr(project, attribute, value)
        project.save()

        def cleanup_project():
            setattr(project, attribute, old_value)
            project.save()

        self.addCleanup(cleanup_project)

# class TestImportExportIntegrity(APITestCase):
#     """Tests that check for equality between imported and exported data of a file. """
#     @classmethod
#     def setUpTestData(cls):
#         cls.super_user_name = 'super_user_name'
#         cls.super_user_pass = 'super_user_pass'
#         create_default_roles()
#         super_user = User.objects.create_superuser(username=cls.super_user_name,
#                                                    password=cls.super_user_pass,
#                                                    email='fizz@buzz.com')
#         cls.classification_project = mommy.make('TextClassificationProject',
#                                                 users=[super_user], project_type=DOCUMENT_CLASSIFICATION)
#
#         cls.classification_upload_url = reverse(viewname='doc_uploader', args=[cls.classification_project.id])
#         cls.classification_download_url = reverse(viewname='doc_downloader', args=[cls.classification_project.id])
#         assign_user_to_role(project_member=super_user, project=cls.classification_project,
#                             role_name=settings.ROLE_PROJECT_ADMIN)
#
#     def setUp(self):
#         self.client.login(username=self.super_user_name,
#                           password=self.super_user_pass)
#
#     def load_test_helper(self, upload_url, download_url, filename, import_format, export_format, response_format="text/csv; charset=utf-8",**kwargs):
#         parser = TextUploadAPI.select_parser(import_format)
#         with open(os.path.join(DATA_DIR, filename), 'rb') as f:
#             self.client.post(upload_url, data={'file': f, 'format': import_format})
#             f.seek(0)
#             imported = parser.parse(f)
#             import_data = [elem for elem in [x for elem in imported for x in elem] if elem.get('labels')]
#
#         r = self.client.get(download_url, data={'q': export_format}, HTTP_ACCEPT=response_format)
#         b = BytesIO(r.content)
#         if export_format == 'txt':
#             export_format = import_format
#         parser = TextUploadAPI.select_parser(export_format)
#         exported = parser.parse(b)
#         exported_data = [x for elem in exported for x in elem if x.get('labels') or x.get('annotations')]
#         self.assertTrue(len(import_data) == len(exported_data), 'Length of imported dataset does not match exported')
#         return import_data, exported_data
#
#     # Classification
#     def test_jsonl_classification_import_export_integrity(self):
#         import_data, export_data = self.load_test_helper(upload_url=self.classification_upload_url,
#                                 download_url=self.classification_download_url,
#                                 filename='classification.jsonl',
#                                 import_format='json',
#                                 project=self.classification_project,
#                                 export_format='json',
#                                 response_format='application/json')
#         label_mapping = {label.id: label.text for label in self.classification_project.labels.all()}
#         for im, ex in zip(import_data, export_data):
#             self.assertTrue(im['text'] == ex['text'], 'Integritycheck failed. Dataset texts do not match.')
#             ex_labels = set(label_mapping[int(x.get('label'))] for x in ex.get('annotations', []))
#             self.assertFalse(set(im.get('labels')).symmetric_difference(ex_labels), 'Integritycheck failed. Labels differ.')
#
#     def test_csv_classification_import_export_integrity(self):
#         import_data, export_data = self.load_test_helper(upload_url=self.classification_upload_url,
#                                 download_url=self.classification_download_url,
#                                 filename='example.csv',
#                                 import_format='csv',
#                                 project=self.classification_project,
#                                 export_format='csv')
#         label_mapping = {label.id: label.text for label in self.classification_project.labels.all()}
#         for im, ex in zip(import_data, export_data):
#             self.assertTrue(im['text'] == ex['text'], 'Integritycheck failed. Dataset texts do not match.')
#             ex_labels = [label_mapping[int(elem)] for elem in ex.get('labels', [])]
#             self.assertTrue(im.get('labels') == ex_labels, 'Integritycheck failed. Labels differ.')
#
#     def test_xlsx_classification_import_export_integrity(self):
#         import_data, export_data = self.load_test_helper(upload_url=self.classification_upload_url,
#                                 download_url=self.classification_download_url,
#                                 filename='example.xlsx',
#                                 import_format='excel',
#                                 project=self.classification_project,
#                                 export_format='csv')
#         label_mapping = {label.id: label.text for label in self.classification_project.labels.all()}
#         for im, ex in zip(import_data, export_data):
#             self.assertTrue(im['text'] == ex['text'], 'Integritycheck failed. Dataset texts do not match.')
#             ex_labels = [label_mapping[int(elem)] for elem in ex.get('labels', [])]
#             self.assertTrue(im.get('labels') == ex_labels, 'Integritycheck failed. Labels differ.')
#
#     def test_fasttext_classification_import_export_integrity(self):
#         import_data, export_data = self.load_test_helper(upload_url=self.classification_upload_url,
#                                 download_url=self.classification_download_url,
#                                 filename='example_fasttext.txt',
#                                 import_format='fastText',
#                                 project=self.classification_project,
#                                 export_format='txt')
#         for im, ex in zip(import_data, export_data):
#             self.assertTrue(im['text'] == ex['text'], 'Integritycheck failed. Dataset texts do not match.')
#             self.assertFalse(set(im.get('labels')).symmetric_difference(ex.get('labels')), 'Integritycheck failed. Labels differ.')
#
#     @classmethod
#     def doCleanups(cls):
#         remove_all_role_mappings()

# class TestUploader(APITestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         cls.super_user_name = 'super_user_name'
#         cls.super_user_pass = 'super_user_pass'
#         # Todo: change super_user to project_admin.
#         create_default_roles()
#         super_user = User.objects.create_superuser(username=cls.super_user_name,
#                                                    password=cls.super_user_pass,
#                                                    email='fizz@buzz.com')
#         cls.classification_project = mommy.make('TextClassificationProject',
#                                                 users=[super_user], project_type=DOCUMENT_CLASSIFICATION)
#         cls.labeling_project = mommy.make('SequenceLabelingProject',
#                                           users=[super_user], project_type=SEQUENCE_LABELING)
#         cls.seq2seq_project = mommy.make('Seq2seqProject', users=[super_user], project_type=SEQ2SEQ)
#         assign_user_to_role(project_member=super_user, project=cls.classification_project,
#                             role_name=settings.ROLE_PROJECT_ADMIN)
#         assign_user_to_role(project_member=super_user, project=cls.labeling_project,
#                             role_name=settings.ROLE_PROJECT_ADMIN)
#         assign_user_to_role(project_member=super_user, project=cls.seq2seq_project,
#                             role_name=settings.ROLE_PROJECT_ADMIN)
#
#     def setUp(self):
#         self.client.login(username=self.super_user_name,
#                           password=self.super_user_pass)
#
#     def upload_test_helper(self, project_id, filename, file_format, expected_status, **kwargs):
#         url = reverse(viewname='doc_uploader', args=[project_id])
#
#         with open(os.path.join(DATA_DIR, filename), 'rb') as f:
#             response = self.client.post(url, data={'file': f, 'format': file_format})
#
#         self.assertEqual(response.status_code, expected_status)
#
#     def label_test_helper(self, project_id, expected_labels, expected_label_keys):
#         url = reverse(viewname='label_list', args=[project_id])
#         expected_keys = {key for label in expected_labels for key in label}
#
#         response = self.client.get(url).json()
#
#         actual_labels = [{key: value for (key, value) in label.items() if key in expected_keys}
#                          for label in response]
#
#         self.assertCountEqual(actual_labels, expected_labels)
#
#         for label in response:
#             for expected_label_key in expected_label_keys:
#                 self.assertIsNotNone(label.get(expected_label_key))
#
#     def test_can_upload_conll_format_file(self):
#         self.upload_test_helper(project_id=self.labeling_project.id,
#                                 filename='labeling.conll',
#                                 file_format='conll',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_cannot_upload_wrong_conll_format_file(self):
#         self.upload_test_helper(project_id=self.labeling_project.id,
#                                 filename='labeling.invalid.conll',
#                                 file_format='conll',
#                                 expected_status=status.HTTP_400_BAD_REQUEST)
#
#     def test_can_upload_classification_csv(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.csv',
#                                 file_format='csv',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_classification_csv_with_out_of_order_columns(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example_out_of_order_columns.csv',
#                                 file_format='csv',
#                                 expected_status=status.HTTP_201_CREATED)
#
#         self.label_test_helper(
#             project_id=self.classification_project.id,
#             expected_labels=[
#                 {'text': 'Positive'},
#                 {'text': 'Negative'},
#             ],
#             expected_label_keys=[],
#         )
#
#     def test_can_upload_csv_with_non_utf8_encoding(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.utf16.csv',
#                                 file_format='csv',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_seq2seq_csv(self):
#         self.upload_test_helper(project_id=self.seq2seq_project.id,
#                                 filename='example.csv',
#                                 file_format='csv',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_single_column_csv(self):
#         self.upload_test_helper(project_id=self.seq2seq_project.id,
#                                 filename='example_one_column.csv',
#                                 file_format='csv',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_csv_file_does_not_match_column_and_row(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example_column_and_row_not_matching.csv',
#                                 file_format='csv',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_cannot_upload_csv_file_has_too_many_columns(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.invalid.2.csv',
#                                 file_format='csv',
#                                 expected_status=status.HTTP_400_BAD_REQUEST)
#
#     def test_can_upload_classification_excel(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.xlsx',
#                                 file_format='excel',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_seq2seq_excel(self):
#         self.upload_test_helper(project_id=self.seq2seq_project.id,
#                                 filename='example.xlsx',
#                                 file_format='excel',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_single_column_excel(self):
#         self.upload_test_helper(project_id=self.seq2seq_project.id,
#                                 filename='example_one_column.xlsx',
#                                 file_format='excel',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_excel_file_does_not_match_column_and_row(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example_column_and_row_not_matching.xlsx',
#                                 file_format='excel',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_cannot_upload_excel_file_has_too_many_columns(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.invalid.2.xlsx',
#                                 file_format='excel',
#                                 expected_status=status.HTTP_400_BAD_REQUEST)
#
#     @override_settings(IMPORT_BATCH_SIZE=1)
#     def test_can_upload_small_batch_size(self):
#         self.upload_test_helper(project_id=self.seq2seq_project.id,
#                                 filename='example_one_column_no_header.xlsx',
#                                 file_format='excel',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_classification_jsonl(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='classification.jsonl',
#                                 file_format='json',
#                                 expected_status=status.HTTP_201_CREATED)
#
#         self.label_test_helper(
#             project_id=self.classification_project.id,
#             expected_labels=[
#                 {'text': 'positive', 'suffix_key': 'p', 'prefix_key': None},
#                 {'text': 'negative', 'suffix_key': 'n', 'prefix_key': None},
#                 {'text': 'neutral', 'suffix_key': 'n', 'prefix_key': 'ctrl'},
#             ],
#             expected_label_keys=[
#                 'background_color',
#                 'text_color',
#             ])
#
#     def test_can_upload_labeling_jsonl(self):
#         self.upload_test_helper(project_id=self.labeling_project.id,
#                                 filename='labeling.jsonl',
#                                 file_format='json',
#                                 expected_status=status.HTTP_201_CREATED)
#
#         self.label_test_helper(
#             project_id=self.labeling_project.id,
#             expected_labels=[
#                 {'text': 'LOC', 'suffix_key': 'l', 'prefix_key': None},
#                 {'text': 'ORG', 'suffix_key': 'o', 'prefix_key': None},
#                 {'text': 'PER', 'suffix_key': 'p', 'prefix_key': None},
#             ],
#             expected_label_keys=[
#                 'background_color',
#                 'text_color',
#             ])
#
#     def test_can_upload_seq2seq_jsonl(self):
#         self.upload_test_helper(project_id=self.seq2seq_project.id,
#                                 filename='seq2seq.jsonl',
#                                 file_format='json',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_plain_text(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.txt',
#                                 file_format='plain',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     def test_can_upload_data_without_label(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.jsonl',
#                                 file_format='json',
#                                 expected_status=status.HTTP_201_CREATED)
#
#     @classmethod
#     def doCleanups(cls):
#         remove_all_role_mappings()


# @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER='LOCAL')
# @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_ACCOUNT=os.path.dirname(DATA_DIR))
# @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_SECRET_KEY='not-used')
# class TestCloudUploader(TestUploader):
#     def upload_test_helper(self, project_id, filename, file_format, expected_status, **kwargs):
#         query_params = {
#             'project_id': project_id,
#             'upload_format': file_format,
#             'container': kwargs.pop('container', os.path.basename(DATA_DIR)),
#             'object': filename,
#         }
#
#         query_params.update(kwargs)
#
#         response = self.client.get(reverse('cloud_uploader'), query_params)
#
#         self.assertEqual(response.status_code, expected_status)
#
#     def test_cannot_upload_with_missing_file(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='does-not-exist',
#                                 file_format='json',
#                                 expected_status=status.HTTP_400_BAD_REQUEST)
#
#     def test_cannot_upload_with_missing_container(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.jsonl',
#                                 container='does-not-exist',
#                                 file_format='json',
#                                 expected_status=status.HTTP_400_BAD_REQUEST)
#
#     def test_cannot_upload_with_missing_query_parameters(self):
#         response = self.client.get(reverse('cloud_uploader'), {'project_id': self.classification_project.id})
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_can_upload_with_redirect(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.jsonl',
#                                 next='http://somewhere',
#                                 file_format='json',
#                                 expected_status=status.HTTP_302_FOUND)
#
#     def test_can_upload_with_redirect_to_blank(self):
#         self.upload_test_helper(project_id=self.classification_project.id,
#                                 filename='example.jsonl',
#                                 next='about:blank',
#                                 file_format='json',
#                                 expected_status=status.HTTP_201_CREATED)


# class TestDownloader(APITestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         cls.super_user_name = 'super_user_name'
#         cls.super_user_pass = 'super_user_pass'
#         # Todo: change super_user to project_admin.
#         create_default_roles()
#         super_user = User.objects.create_superuser(username=cls.super_user_name,
#                                                    password=cls.super_user_pass,
#                                                    email='fizz@buzz.com')
#         cls.classification_project = mommy.make('TextClassificationProject',
#                                                 users=[super_user], project_type=DOCUMENT_CLASSIFICATION)
#         cls.labeling_project = mommy.make('SequenceLabelingProject',
#                                           users=[super_user], project_type=SEQUENCE_LABELING)
#         cls.seq2seq_project = mommy.make('Seq2seqProject', users=[super_user], project_type=SEQ2SEQ)
#         cls.speech2text_project = mommy.make('Speech2textProject', users=[super_user], project_type=SPEECH2TEXT)
#         cls.classification_url = reverse(viewname='doc_downloader', args=[cls.classification_project.id])
#         cls.labeling_url = reverse(viewname='doc_downloader', args=[cls.labeling_project.id])
#         cls.seq2seq_url = reverse(viewname='doc_downloader', args=[cls.seq2seq_project.id])
#         cls.speech2text_url = reverse(viewname='doc_downloader', args=[cls.speech2text_project.id])
#
#     def setUp(self):
#         self.client.login(username=self.super_user_name,
#                           password=self.super_user_pass)
#
#     def download_test_helper(self, url, format, expected_status):
#         response = self.client.get(url, data={'q': format})
#         self.assertEqual(response.status_code, expected_status)
#
#     def test_cannot_download_conll_format_file(self):
#         self.download_test_helper(url=self.labeling_url,
#                                   format='conll',
#                                   expected_status=status.HTTP_400_BAD_REQUEST)
#
#     def test_can_download_classification_csv(self):
#         self.download_test_helper(url=self.classification_url,
#                                   format='csv',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_labeling_csv(self):
#         self.download_test_helper(url=self.labeling_url,
#                                   format='csv',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_seq2seq_csv(self):
#         self.download_test_helper(url=self.seq2seq_url,
#                                   format='csv',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_classification_jsonl(self):
#         self.download_test_helper(url=self.classification_url,
#                                   format='json',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_labeling_jsonl(self):
#         self.download_test_helper(url=self.labeling_url,
#                                   format='json',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_seq2seq_jsonl(self):
#         self.download_test_helper(url=self.seq2seq_url,
#                                   format='json',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_speech2text_jsonl(self):
#         self.download_test_helper(url=self.speech2text_url,
#                                   format='json',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_labelling_jsonl(self):
#         self.download_test_helper(url=self.labeling_url,
#                                   format='jsonl',
#                                   expected_status=status.HTTP_200_OK)
#
#     def test_can_download_plain_text(self):
#         self.download_test_helper(url=self.classification_url,
#                                   format='plain',
#                                   expected_status=status.HTTP_400_BAD_REQUEST)
#
#     def test_can_download_classification_fasttext(self):
#         self.download_test_helper(url=self.classification_url,
#                                     format='txt',
#                                     expected_status=status.HTTP_200_OK)


