from django.conf import settings
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail

from projects.models import (
    Answer,
    OptionQuestion,
    OptionsGroup,
    Perspective,
    Question,
    QuestionType,
    Member
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
    serializer_class = PerspectiveSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("members__user__username",)

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Perspective.objects.filter(project_id=project_id)


class PerspectiveCreation(generics.CreateAPIView):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def create(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")
        if project_id and Perspective.objects.filter(project_id=project_id).exists():
            return Response(
                {"error": "Este projeto já tem uma perspectiva"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                # Retornar erros de validação específicos
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            perspective = self.perform_create(serializer)

            questions_data = request.data.get("questions", [])
            for question_data in questions_data:
                question_data["perspective"] = perspective.id
                question_serializer = QuestionSerializer(data=question_data)
                question_serializer.is_valid(raise_exception=True)
                question_serializer.save()
            members_ids = request.data.get("members", [])
            members = Member.objects.filter(id__in=members_ids).select_related("user")
            recipients = [member.user.email for member in members if member.user.email]
            if recipients:
                subject = 'Perspective of the project created'
                message = 'You have to add your perspective to the project'
                self.send_notification_email(recipients, subject, message)
            return Response(PerspectiveSerializer(perspective).data, status=status.HTTP_201_CREATED)
        
    def send_notification_email(self, recipients, subject, message):
        if not recipients:
            return False
        try:
            send_mail(
               subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipients,
                fail_silently=False,
        )
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False   
     

    def perform_create(self, serializer):
        return serializer.save()


class Answers(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # Optionally, you can also use filterset_fields for other filtering
    filterset_fields = ['question']
    search_fields = ("question__id", "member__user__username", "answer_text", "answer_option")

    def get_queryset(self):
        queryset = Answer.objects.all()
        # Get the selected question id from query parameters
        question_id = self.request.query_params.get('question_id')
        if question_id:
            queryset = queryset.filter(question__id=question_id)
        return queryset


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
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("perspective__id", "question")

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        perspective_id = self.kwargs.get('perspective_id')
        return Question.objects.filter(perspective_id=perspective_id, perspective__project_id=project_id)


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
    serializer_class = OptionQuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("option", "options_group__name")

    def get_queryset(self):
        # Note: OptionsGroup não tem project_id, pode ser que precise de um filtro diferente
        # Por agora, retornando todos para não quebrar a funcionalidade
        return OptionQuestion.objects.all()


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
    serializer_class = OptionsGroupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("name",)

    def get_queryset(self):
        # Note: OptionsGroup não tem project_id diretamente
        # Por agora, retornando todos para não quebrar a funcionalidade
        return OptionsGroup.objects.all()


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
