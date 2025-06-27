from rest_framework import serializers

from .models import Assignment, Comment, Example, ExampleState


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "username",
            "example",
            "text",
            "created_at",
        )
        read_only_fields = ("user", "example")


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ("id", "assignee", "example", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class ExampleSerializer(serializers.ModelSerializer):
    annotation_approver = serializers.SerializerMethodField()
    is_confirmed = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()

    @classmethod
    def get_annotation_approver(cls, instance):
        approver = instance.annotations_approved_by
        return approver.username if approver else None

    def get_is_confirmed(self, instance):
        user = self.context.get("request").user
        if instance.project.collaborative_annotation:
            states = instance.states.all()
        else:
            states = instance.states.filter(confirmed_by_id=user.id)
        return states.count() > 0

    def get_assignments(self, instance):
        return [
            {
                "id": assignment.id,
                "assignee": assignment.assignee.username,
                "assignee_id": assignment.assignee.id,
            }
            for assignment in instance.assignments.all()
        ]

    def get_annotations(self, instance):
        request = self.context.get("request")
        if not request or not request.query_params.get("include_annotation"):
            return []

        annotations = []

        # Buscar categorias
        for category in instance.categories.all():
            annotations.append({
                "user": category.user.id,
                "user_id": category.user.id,
                "created_by": category.user.id,
                "label": category.label.text if category.label else None,
                "type": "category"
            })

        # Buscar spans
        for span in instance.spans.all():
            annotations.append({
                "user": span.user.id,
                "user_id": span.user.id,
                "created_by": span.user.id,
                "label": span.label.text if span.label else None,
                "start_offset": span.start_offset,
                "end_offset": span.end_offset,
                "type": "span"
            })

        # Buscar relations
        for relation in instance.relations.all():
            annotations.append({
                "user": relation.user.id,
                "user_id": relation.user.id,
                "created_by": relation.user.id,
                "label": relation.type.text if relation.type else None,
                "type": "relation"
            })

        # Buscar text labels
        for text_label in instance.texts.all():
            annotations.append({
                "user": text_label.user.id,
                "user_id": text_label.user.id,
                "created_by": text_label.user.id,
                "text": text_label.text,
                "type": "text"
            })

        return annotations

    class Meta:
        model = Example
        fields = [
            "id",
            "filename",
            "meta",
            "annotation_approver",
            "comment_count",
            "text",
            "is_confirmed",
            "upload_name",
            "score",
            "assignments",
            "annotations",
        ]
        read_only_fields = ["filename", "is_confirmed", "upload_name", "assignments", "annotations"]


class ExampleStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleState
        fields = ("id", "example", "confirmed_by", "confirmed_at")
        read_only_fields = ("id", "example", "confirmed_by", "confirmed_at")
