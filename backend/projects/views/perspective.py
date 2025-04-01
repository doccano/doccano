from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from projects.models import (
    Answer,
    OptionQuestion,
    OptionsGroup,
    Perspective,
    Question,
    QuestionType,
)
from projects.permissions import IsProjectAdmin
from projects.serializers import (
    AnswerSerializer,
    OptionQuestionSerializer,
    OptionsGroupSerializer,
    PerspectiveSerializer,
    QuestionSerializer,
    QuestionTypeSerializer,
)


class Perspectives(generics.ListAPIView):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("members__user__username",)


class PerspectiveCreation(generics.CreateAPIView):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def create(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")
        if project_id and Perspective.objects.filter(project_id=project_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            perspective = self.perform_create(serializer)

            questions_data = request.data.get("questions", [])
            for question_data in questions_data:
                question_data["perspective"] = perspective.id
                question_serializer = QuestionSerializer(data=question_data)
                question_serializer.is_valid(raise_exception=True)
                question_serializer.save()

            return Response(PerspectiveSerializer(perspective).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()


class Answers(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("question__id", "member__user__username", "answer_text", "answer_option")


class AnswerCreation(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        answer = serializer.save()
        return answer


class Questions(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("perspective__id", "question")


class AnswerNestedSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ("id", "answer", "member")


class QuestionNestedSerializer(serializers.ModelSerializer):
    answers = AnswerNestedSerializer(many=True, read_only=True, source="answer_set")

    class Meta:
        model = Question
        fields = ("id", "question", "answers")


class PerspectiveDetailSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(many=True, read_only=True, source="question_set")

    class Meta:
        model = Perspective
        fields = ("id", "name", "questions")


class PerspectiveDetail(RetrieveAPIView):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveDetailSerializer
    permission_classes = [IsAuthenticated]


class OptionsQuestion(generics.ListAPIView):
    queryset = OptionQuestion.objects.all()
    serializer_class = OptionQuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("option", "options_group__name")


class OptionsQuestionCreation(generics.CreateAPIView):
    queryset = OptionQuestion.objects.all()
    serializer_class = OptionQuestionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option_question = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(OptionQuestionSerializer(option_question).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class OptionsGroups(generics.ListAPIView):
    queryset = OptionsGroup.objects.all()
    serializer_class = OptionsGroupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("name",)


class OptionsGroupsCreation(generics.CreateAPIView):
    queryset = OptionsGroup.objects.all()
    serializer_class = OptionsGroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        options_group = self.perform_create(serializer)
        options_questions_data = self.request.data.get("options_questions", [])
        options_group = serializer.save()

        for option_data in options_questions_data:
            option_data["options_group"] = options_group.id
            option_question_serializer = OptionQuestionSerializer(data=option_data)
            option_question_serializer.is_valid(raise_exception=True)
            option_question_serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(OptionsGroupSerializer(options_group).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class OptionsGroupDetail(generics.RetrieveAPIView):
    serializer_class = OptionsGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        group_name = self.kwargs["group_name"]
        try:
            return OptionsGroup.objects.get(name=group_name)
        except OptionsGroup.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class QuestionsType(generics.ListAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("question_type",)


class QuestionsTypeCreation(generics.CreateAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option_question = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(QuestionTypeSerializer(option_question).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class QuestionsTypeDetail(generics.RetrieveAPIView):
    serializer_class = QuestionTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        question_type_id = self.kwargs["question_type_id"]
        try:
            return QuestionType.objects.get(id=question_type_id)
        except QuestionType.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(obj)
        return Response(serializer.data)
