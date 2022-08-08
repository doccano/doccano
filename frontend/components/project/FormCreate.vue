<template>
  <v-card>
    <v-card-title>{{ $t('overview.createProjectTitle') }}</v-card-title>
    <v-card-text>
      <v-form v-model="valid">
        <v-item-group
          v-model="selected"
          mandatory
          @change="updateValue('projectType', projectTypes[selected])"
        >
          <v-row no-gutters>
            <v-col v-for="(item, i) in projectTypes" :key="i">
              <v-item v-slot="{ active, toggle }">
                <v-card class="mb-6 me-6" max-width="350" outlined>
                  <v-img
                    :src="require(`~/assets/images/tasks/${images[i]}`)"
                    height="200"
                    contain
                    @click="toggle"
                  />
                  <v-card-title>
                    <v-icon v-if="active">
                      {{ mdiCheckBold }}
                    </v-icon>
                    {{ translateTypeName(item, $t('overview.projectTypes')) }}
                  </v-card-title>
                </v-card>
              </v-item>
            </v-col>
          </v-row>
        </v-item-group>

        <v-text-field
          :value="name"
          :rules="projectNameRules($t('rules.projectNameRules'))"
          :label="$t('overview.projectName')"
          outlined
          required
          autofocus
          @input="updateValue('name', $event)"
        />
        <v-text-field
          :value="description"
          :rules="descriptionRules($t('rules.descriptionRules'))"
          :label="$t('generic.description')"
          outlined
          required
          @input="updateValue('description', $event)"
        />
        <v-combobox
          :value="tags"
          :items="tags"
          label="Tags"
          multiple
          chips
          outlined
          dense
          deletable-chips
          hide-selected
          @input="updateValue('tags', $event)"
        />
        <v-checkbox
          v-if="hasSingleLabelOption"
          :value="singleClassClassification"
          :label="$t('overview.allowSingleLabel')"
          @change="updateValue('singleClassClassification', $event === true)"
        />
        <v-checkbox
          v-if="isSequenceLabelingProject"
          :value="allowOverlapping"
          label="Allow overlapping entity"
          @change="updateValue('allowOverlapping', $event === true)"
        />
        <v-img
          v-if="isSequenceLabelingProject"
          :src="require('~/assets/project/creation.gif')"
          height="200"
          position="left"
          contain
        />
        <v-checkbox
          v-if="isSequenceLabelingProject"
          :value="useRelation"
          label="Use relation labeling"
          @change="updateValue('useRelation', $event === true)"
        />
        <v-checkbox
          v-if="isSequenceLabelingProject"
          :value="graphemeMode"
          @change="updateValue('graphemeMode', $event === true)"
        >
          <template #label>
            <div>
              Count
              <v-tooltip bottom>
                <template #activator="{ on }">
                  <a target="_blank" href="https://unicode.org/reports/tr29/" @click.stop v-on="on">
                    grapheme clusters
                  </a>
                </template>
                Like emoji(🌷, 💩, and 👍), CRLF(\r\n), and so on.
              </v-tooltip>
              as one character
            </div>
          </template>
        </v-checkbox>
        <v-checkbox
          :value="enableRandomOrder"
          :label="$t('overview.randomizeDocOrder')"
          @change="updateValue('enableRandomOrder', $event === true)"
        />
        <v-checkbox
          :value="enableShareAnnotation"
          :label="$t('overview.shareAnnotations')"
          @change="updateValue('enableShareAnnotation', $event === true)"
        />
      </v-form>
    </v-card-text>
    <v-card-actions class="ps-4">
      <v-btn
        :disabled="!valid"
        color="primary"
        style="text-transform: none"
        outlined
        @click="$emit('save')"
      >
        {{ $t('generic.create') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiCheckBold } from '@mdi/js'
import { projectNameRules, descriptionRules, projectTypeRules } from '@/rules/index'

export default Vue.extend({
  props: {
    name: {
      type: String,
      default: '',
      required: true
    },
    description: {
      type: String,
      default: '',
      required: true
    },
    projectType: {
      type: String,
      default: '',
      required: true
    },
    enableRandomOrder: {
      type: Boolean,
      default: false,
      required: true
    },
    enableShareAnnotation: {
      type: Boolean,
      default: false,
      required: true
    },
    singleClassClassification: {
      type: Boolean,
      default: false,
      required: true
    },
    allowOverlapping: {
      type: Boolean,
      default: false
    },
    graphemeMode: {
      type: Boolean,
      default: false
    },
    useRelation: {
      type: Boolean,
      default: false
    },
    tags: {
      type: Array,
      default: () => []
    }
  },

  data() {
    return {
      valid: false,
      projectNameRules,
      projectTypeRules,
      descriptionRules,
      mdiCheckBold,
      selected: 0
    }
  },

  computed: {
    projectTypes() {
      return [
        'DocumentClassification',
        'SequenceLabeling',
        'Seq2seq',
        'IntentDetectionAndSlotFilling',
        'ImageClassification',
        'ImageCaptioning',
        'BoundingBox',
        'Segmentation',
        'Speech2text'
      ]
    },
    images() {
      return [
        'text_classification.png',
        'sequence_labeling.png',
        'seq2seq.png',
        'intent_detection.png',
        'image_classification.png',
        'image_captioning.jpg',
        'object_detection.jpg',
        'segmentation.jpg',
        'speech_to_text.png'
      ]
    },
    hasSingleLabelOption() {
      return ['DocumentClassification', 'ImageClassification'].includes(this.projectType)
    },
    isSequenceLabelingProject() {
      return this.projectType === 'SequenceLabeling'
    }
  },

  methods: {
    updateValue(key: string, value: string) {
      this.$emit(`update:${key}`, value)
    },
    translateTypeName(type: string, types: string[]): string {
      const index = this.projectTypes.indexOf(type)
      return types[index]
    }
  }
})
</script>
