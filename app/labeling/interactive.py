# Source : https://github.com/explosion/spaCy/blob/master/examples/training/train_ner.py
from api.serializers import DocumentSerializer
import spacy
from spacy.util import minibatch, compounding
import random


class ProjectInteraction(object):

    def auto_label_documents(self, queryset, project, user_id):
        if project.get_bundle_name() == 'sequence_labeling':
            return self.auto_label_seq_labeling(queryset, project, user_id)
        if project.get_bundle_name() == 'document_classification':
            return self.auto_label_document_classification(queryset, project, user_id)
        else:
            return []

    def auto_label_document_classification(self, queryset, project, user_id):
        print('auto labeling not implemented yet for doc classification')
        return []

    def auto_label_seq_labeling(self, queryset, project, user_id):
        """ Auto labeling for sequence labeling projects based on spaCy's
        multi-language ner
        """
        labelled_data = DocumentSerializer(queryset.exclude(annotations_approved_by=None), many=True).data
        unlabelled_data = DocumentSerializer(queryset.filter(annotations_approved_by=None), many=True).data
        labels = project.labels.all()

        nlp = spacy.load("xx_ent_wiki_sm")
        nlp.remove_pipe('ner')
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)

        labels_id2txt = {}
        labels_txt2label = {}
        for i in range(len(labels)):
            ner.add_label(labels[i].text)
            labels_id2txt[labels[i].id] = labels[i].text
            labels_txt2label[labels[i].text] = labels[i]

        train_data = []
        for item in labelled_data:
            doc = str(nlp.make_doc(item['text']))
            entities = [(x['start_offset'], x['end_offset'], labels_id2txt[x['label']]) for x in item['annotations']]
            train_data.append((doc, {"entities": entities}))

        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):
            sizes = compounding(1.0, 4.0, 1.001)
            optimizer = nlp.begin_training()
            for itn in range(20):
                random.shuffle(train_data)
                batches = minibatch(train_data, size=sizes)
                losses = {}
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
                print("Losses", losses)

        new_data = []
        for item in unlabelled_data:
            doc = str(nlp.make_doc(item['text']))
            entities = [(x['start_offset'], x['end_offset'], labels_id2txt[x['label']]) for x in item['annotations']]
            new_data.append((doc, {"entities": entities}))

        new_sent_annotations = []
        for new, document in zip(new_data, queryset.filter(annotations_approved_by=None)):
            text, _ = new
            doc = nlp(text)
            new_annotations = [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]
            for new in new_annotations:
                new_sent_annotations.append({'document': document,
                                             'label': labels_txt2label[new[1]],
                                             'start_offset': new[2],
                                             'end_offset': new[3],
                                             'user_id': user_id})

        return new_sent_annotations
