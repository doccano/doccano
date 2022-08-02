<template>
  <form-create v-slot="slotProps" v-bind.sync="editedItem" :items="items">
    <v-btn :disabled="!slotProps.valid" color="primary" class="text-capitalize" @click="save">
      Save
    </v-btn>

    <v-btn
      :disabled="!slotProps.valid"
      color="primary"
      style="text-transform: none"
      outlined
      @click="saveAndAnother"
    >
      Save and add another
    </v-btn>
  </form-create>
</template>

<script lang="ts">
import Vue from 'vue'
import { ProjectDTO } from '~/services/application/project/projectData'
import { LabelItem } from '~/domain/models/label/label'
import { LabelRepository } from '~/domain/models/label/labelRepository'
import FormCreate from '~/components/label/FormCreate.vue'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'project',

  validate({ params, query, app }) {
    if (!['category', 'span', 'relation'].includes(query.type as string)) {
      return false
    }
    if (/^\d+$/.test(params.id)) {
      return app.$services.project.findById(params.id).then((res: ProjectDTO) => {
        return res.canDefineLabel
      })
    }
    return false
  },

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
      return this.$repositories[`${type}Type`]
    }
  },

  async created() {
    this.items = await this.repository.list(this.projectId)
  },

  methods: {
    async save() {
      await this.repository.create(this.projectId, this.editedItem)
      this.$router.push(`/projects/${this.projectId}/labels`)
    },

    async saveAndAnother() {
      await this.repository.create(this.projectId, this.editedItem)
      this.editedItem = LabelItem.create()
      this.items = await this.repository.list(this.projectId)
    }
  }
})
</script>
