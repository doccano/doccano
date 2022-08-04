<template>
  <form-create v-slot="slotProps" v-bind.sync="editedItem" :items="items">
    <v-btn :disabled="!slotProps.valid" color="primary" class="text-capitalize" @click="save">
      Save
    </v-btn>
  </form-create>
</template>

<script lang="ts">
import Vue from 'vue'
import FormCreate from '~/components/label/FormCreate.vue'
import { validateEditPage } from '~/plugins/labelType/validators'
import { LabelItem } from '~/domain/models/label/label'
import { LabelRepository } from '~/domain/models/label/labelRepository'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'project',

  validate: validateEditPage,

  data() {
    return {
      editedItem: LabelItem.create(),
      items: [] as LabelItem[]
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    repository(): LabelRepository {
      const type = this.$route.query.type
      if (type === 'category') {
        return this.$repositories.categoryType
      } else if (type === 'span') {
        return this.$repositories.spanType
      } else {
        return this.$repositories.relationType
      }
    }
  },

  async created() {
    const labelId = this.$route.params.label_id
    this.items = await this.repository.list(this.projectId)
    this.editedItem = await this.repository.findById(this.projectId, parseInt(labelId))
  },

  methods: {
    async save() {
      await this.repository.update(this.projectId, this.editedItem)
      this.$router.push(`/projects/${this.projectId}/labels`)
    }
  }
})
</script>
