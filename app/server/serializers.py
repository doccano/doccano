from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Label, Project, Document
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation, DocumentMLMAnnotation


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'text', 'comment', 'shortcut', 'background_color', 'text_color')


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('id', 'text')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')

class ProjectSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at', 'use_machine_model_sort', 'progress', 'enable_metadata_search', 'show_ml_model_prediction')

    def get_progress(self, obj):
        request = self.context.get('request')
        return obj.get_progress(request.user)


class ProjectFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        view = self.context.get('view', None)
        request = self.context.get('request', None)
        queryset = super(ProjectFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset or not view:
            return None
        return queryset.filter(project=view.kwargs['project_id'])


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = DocumentAnnotation
        fields = ('id', 'prob', 'label')

    def create(self, validated_data):
        annotation = DocumentAnnotation.objects.create(**validated_data)
        return annotation

class DocumentMLMAnnotationSerializer(serializers.ModelSerializer):
    label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = DocumentMLMAnnotation
        fields = ('id', 'prob', 'label')

    def create(self, validated_data):
        annotation = DocumentMLMAnnotation.objects.create(**validated_data)
        return annotation


class SequenceAnnotationSerializer(serializers.ModelSerializer):
    label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = SequenceAnnotation
        fields = ('id', 'prob', 'label', 'start_offset', 'end_offset')

    def create(self, validated_data):
        annotation = SequenceAnnotation.objects.create(**validated_data)
        return annotation


class Seq2seqAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seq2seqAnnotation
        fields = ('id', 'text')


class ClassificationDocumentSerializer(serializers.ModelSerializer):
    annotations = serializers.SerializerMethodField()
    mlm_annotations = serializers.SerializerMethodField()

    def get_annotations(self, instance):
        request = self.context.get('request')
        if request:
            annotations = instance.doc_annotations.filter(user=request.user)
            serializer = DocumentAnnotationSerializer(annotations, many=True)
            return serializer.data

    def get_mlm_annotations(self, instance):
        request = self.context.get('request')
        if request:
            annotations = instance.doc_mlm_annotations
            serializer = DocumentMLMAnnotationSerializer(annotations, many=True)
            return serializer.data

    class Meta:
        model = Document
        fields = ('id', 'text', 'annotations', 'metadata', 'mlm_annotations')


class SequenceDocumentSerializer(serializers.ModelSerializer):
    annotations = serializers.SerializerMethodField()

    def get_annotations(self, instance):
        request = self.context.get('request')
        if request:
            annotations = instance.seq_annotations.filter(user=request.user)
            serializer = SequenceAnnotationSerializer(annotations, many=True)
            return serializer.data

    class Meta:
        model = Document
        fields = ('id', 'text', 'annotations')


class Seq2seqDocumentSerializer(serializers.ModelSerializer):
    annotations = serializers.SerializerMethodField()

    def get_annotations(self, instance):
        request = self.context.get('request')
        if request:
            annotations = instance.seq2seq_annotations.filter(user=request.user)
            serializer = Seq2seqAnnotationSerializer(annotations, many=True)
            return serializer.data

    class Meta:
        model = Document
        fields = ('id', 'text', 'annotations')


class Word2vecSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id',)