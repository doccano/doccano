<template>
  <layout-text v-if="example.id">
    <template #header>
      <toolbar-laptop
        :doc-id="example.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="example.isConfirmed"
        :total="totalExample"
        class="d-none d-sm-block"
        @click:clear-label="clearTeacherList(project.id, example.id)"
        @click:review="confirm(project.id)"
      >
        <button-label-switch class="ms-2" @change="labelComponent = $event" />
      </toolbar-laptop>
      <toolbar-mobile :total="totalExample" class="d-flex d-sm-none" />
    </template>
    <template #content>
      <v-card
        v-shortkey="shortKeys"
        @shortkey="annotateOrRemoveLabel(project.id, example.id, $event.srcKey)"
      >
        <v-card-title>
          <component
            :is="labelComponent"
            :labels="labels"
            :annotations="teacherList"
            :single-label="project.singleClassClassification"
            @add="annotateLabel(project.id, example.id, $event)"
            @remove="removeTeacher(project.id, example.id, $event)"
          />
        </v-card-title>
        <v-divider />
        <v-card-text class="title highlight" style="white-space: pre-wrap" v-text="example.text" />
      </v-card>
    </template>
    <template #sidebar>
      <annotation-progress :progress="progress" />
      <list-metadata :metadata="example.meta" class="mt-4" />
    </template>
  </layout-text>
</template>

<script>
import { ref, toRefs, useContext, useFetch, watch } from '@nuxtjs/composition-api'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import AnnotationProgress from '@/components/tasks/sidebar/AnnotationProgress.vue'
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'
import LabelSelect from '@/components/tasks/textClassification/LabelSelect'
import ButtonLabelSwitch from '@/components/tasks/toolbar/buttons/ButtonLabelSwitch'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import { useExampleItem } from '@/composables/useExampleItem'
import { useLabelList } from '@/composables/useLabelList'
import { useProjectItem } from '@/composables/useProjectItem'
import { useTeacherList } from '@/composables/useTeacherList'

export default {
  components: {
    AnnotationProgress,
    ButtonLabelSwitch,
    LabelGroup,
    LabelSelect,
    LayoutText,
    ListMetadata,
    ToolbarLaptop,
    ToolbarMobile
  },
  layout: 'workspace',

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  },

  setup() {
    const { app, params, query } = useContext()
    const projectId = params.value.id
    const { state: projectState, getProjectById } = useProjectItem()
    const { state: exampleState, confirm, getExample, updateProgress } = useExampleItem()
    const {
      state: teacherState,
      annotateLabel,
      annotateOrRemoveLabel,
      autoLabel,
      clearTeacherList,
      getTeacherList,
      removeTeacher
    } = useTeacherList(app.$repositories.category)
    const enableAutoLabeling = ref(false)
    const { state: labelState, getLabelList, shortKeys } = useLabelList(app.$services.categoryType)
    const labelComponent = ref('label-group')

    getLabelList(projectId)
    getProjectById(projectId)
    updateProgress(projectId)

    const { fetch } = useFetch(async () => {
      await getExample(projectId, query.value)
      if (enableAutoLabeling.value) {
        try {
          await autoLabel(projectId, exampleState.example.id)
        } catch (e) {
          enableAutoLabeling.value = false
          alert(e.response.data.detail)
        }
      } else {
        await getTeacherList(projectId, exampleState.example.id)
      }
    })
    watch(query, fetch)
    watch(enableAutoLabeling, async (val) => {
      if (val && !exampleState.example.isConfirmed) {
        await autoLabel(exampleState.example.id)
        await getTeacherList(exampleState.example.id)
      }
    })

    return {
      ...toRefs(labelState),
      ...toRefs(projectState),
      ...toRefs(teacherState),
      ...toRefs(exampleState),
      confirm,
      annotateLabel,
      annotateOrRemoveLabel,
      clearTeacherList,
      enableAutoLabeling,
      labelComponent,
      removeTeacher,
      shortKeys
    }
  }
}
</script>
