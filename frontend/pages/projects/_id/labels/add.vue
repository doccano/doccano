<template>
  <form-create v-slot="slotProps" v-bind.sync="editedItem" :items="labelTypes">
    <v-btn
      :disabled="!slotProps.valid"
      color="primary"
      class="text-capitalize"
      @click="save(projectId)"
    >
      Save
    </v-btn>

    <v-btn
      :disabled="!slotProps.valid"
      color="primary"
      style="text-transform: none"
      outlined
      @click="saveAndAnother(projectId)"
    >
      Save and add another
    </v-btn>
  </form-create>
</template>

<script lang="ts">
import { useContext, defineComponent } from '@nuxtjs/composition-api'
import FormCreate from '~/components/label/FormCreate.vue'
import { useFormCreate } from '~/composables/labelType/useFormCreate'
import { validateItemPage } from '~/plugins/labelType/validators'

export default defineComponent({
  components: {
    FormCreate
  },

  layout: 'project',

  validate: validateItemPage,

  setup() {
    const { app, params, query } = useContext()
    const projectId = params.value.id
    const repository = app.$repositories[`${query.value.type}Type`]
    const { labelTypes, editedItem, save, saveAndAnother, fetchLabelTypes } =
      useFormCreate(repository)
    fetchLabelTypes(projectId)

    return {
      projectId,
      labelTypes,
      editedItem,
      save,
      saveAndAnother
    }
  }
})
</script>
