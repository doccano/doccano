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
import FormCreate from '~/components/label/FormCreate.vue'
import { Project } from '~/domain/models/project/project'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, query, store }) {
    if (!['category', 'span', 'relation'].includes(query.type as string)) {
      return false
    }
    if (/^\d+$/.test(params.id)) {
      const project = store.getters['projects/project'] as Project
      return project.canDefineLabel
    }
    return false
  },

  data() {
    return {
      editedItem: {
        text: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#73D8FF',
        textColor: '#ffffff'
      } as LabelDTO,
      defaultItem: {
        text: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#73D8FF',
        textColor: '#ffffff'
      } as LabelDTO,
      items: [] as LabelDTO[]
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    service(): any {
      const type = this.$route.query.type
      if (type === 'category') {
        return this.$services.categoryType
      } else if (type === 'span') {
        return this.$services.spanType
      } else {
        return this.$services.relationType
      }
    }
  },

  async created() {
    this.items = await this.service.list(this.projectId)
  },

  methods: {
    async save() {
      await this.service.create(this.projectId, this.editedItem)
      this.$router.push(`/projects/${this.projectId}/labels`)
    },

    async saveAndAnother() {
      await this.service.create(this.projectId, this.editedItem)
      this.editedItem = Object.assign({}, this.defaultItem)
      this.items = await this.service.list(this.projectId)
    }
  }
})
</script>
