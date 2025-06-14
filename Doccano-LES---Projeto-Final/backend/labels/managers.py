from django.db.models import Count, Manager


class LabelManager(Manager):
    label_type_field = "label"

    def calc_label_distribution(self, examples, members, labels):
        """Calculate label distribution.

        Args:
            examples: example queryset.
            members: user queryset.
            labels: label queryset.

        Returns:
            label distribution per user.

        Examples:
            >>> self.calc_label_distribution(examples, members, labels)
            {'admin': {'positive': 10, 'negative': 5}}
        """
        distribution = {member.username: {label.text: 0 for label in labels} for member in members}
        items = (
            self.filter(example_id__in=examples)
            .values("user__username", f"{self.label_type_field}__text")
            .annotate(count=Count(f"{self.label_type_field}__text"))
        )
        for item in items:
            username = item["user__username"]
            label = item[f"{self.label_type_field}__text"]
            count = item["count"]
            distribution[username][label] = count
        return distribution

    def get_label_percentage(self, examples, labels):
        """Calculate label distribution as percentages per example.

        Args:
            examples: example queryset.
            labels: label queryset.

        Returns:
            Dictionary with percentage of each label per example.

        Examples:
            >>> self.get_label_percentage(examples, labels)
            {'example_1': {'positive': 66.7, 'negative': 33.3}, 'example_2': {'positive': 50.0, 'negative': 50.0}}
        """
        percentage = {example: {label.text: 0.0 for label in labels} for example in examples}

        items = (
            self.filter(example_id__in=examples)
            .values("example_id", f"{self.label_type_field}__text")
            .annotate(count=Count(f"{self.label_type_field}__text"))
        )

        example_totals = {example: 0 for example in examples}

        for item in items:
            example_id = item["example_id"]
            label = item[f"{self.label_type_field}__text"]
            count = item["count"]
            percentage[example_id][label] = count
            example_totals[example_id] += count

        # Convert counts to percentages
        for example_id, labels in percentage.items():
            total = example_totals[example_id]
            if total > 0:
                for label in labels:
                    labels[label] = (labels[label] / total) * 100  # Calcula a percentagem
        return percentage

    def get_labels(self, label, project):
        if project.collaborative_annotation:
            return self.filter(example=label.example)
        else:
            return self.filter(example=label.example, user=label.user)

    def can_annotate(self, label, project) -> bool:
        raise NotImplementedError("Please implement this method in the subclass")

    def filter_annotatable_labels(self, labels, project):
        return [label for label in labels if self.can_annotate(label, project)]


class CategoryManager(LabelManager):
    def can_annotate(self, label, project) -> bool:
        is_exclusive = project.single_class_classification
        categories = self.get_labels(label, project)
        if is_exclusive:
            return not categories.exists()
        else:
            return not categories.filter(label=label.label).exists()


class SpanManager(LabelManager):
    def can_annotate(self, label, project) -> bool:
        overlapping = getattr(project, "allow_overlapping", False)
        spans = self.get_labels(label, project)
        if overlapping:
            return True
        for span in spans:
            if span.is_overlapping(label):
                return False
        return True


class TextLabelManager(LabelManager):
    def can_annotate(self, label, project) -> bool:
        texts = self.get_labels(label, project)
        for text in texts:
            if text.is_same_text(label):
                return False
        return True


class RelationManager(LabelManager):
    label_type_field = "type"

    def can_annotate(self, label, project) -> bool:
        return True


class BoundingBoxManager(LabelManager):
    def can_annotate(self, label, project) -> bool:
        return True


class SegmentationManager(LabelManager):
    def can_annotate(self, label, project) -> bool:
        return True
