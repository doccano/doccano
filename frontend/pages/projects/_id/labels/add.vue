<template>
  <form-create
    v-slot="slotProps"
    v-bind.sync="editedItem"
    :items="items"
  >
    <v-btn
      :disabled="!slotProps.valid"
      color="primary"
      class="text-capitalize"
      @click="save"
    >
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
import { LabelDTO } from '~/services/application/label/labelData'
import { ProjectDTO } from '~/services/application/project/projectData'
import FormCreate from '~/components/label/FormCreate.vue'

export default Vue.extend({
  components: {
    FormCreate,
  },

  layout: 'project',

  validate({ params, query, app }) {
    if (!['category', 'span'].includes((query.type as string))) {
      return false
    }
    if (/^\d+$/.test(params.id)) {
      return app.$services.project.findById(params.id)
      .then((res:ProjectDTO) => {
        return res.canDefineLabel
      })
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
      } else {
        return this.$services.spanType
      }
    },
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
