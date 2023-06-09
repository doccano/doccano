<template>
  <v-card>
    <v-tabs v-if="hasMultiType" v-model="tab">
      <template v-if="isIntentDetectionAndSlotFilling">
        <v-tab class="text-capitalize">Category</v-tab>
        <v-tab class="text-capitalize">Span</v-tab>
      </template>
      <template v-else>
        <v-tab class="text-capitalize">Span</v-tab>
        <v-tab class="text-capitalize">Relation</v-tab>
      </template>
    </v-tabs>
    <v-card-title>
      <action-menu
        :add-only="canOnlyAdd"
        @create="$router.push('labels/add?type=' + labelType)"
        @upload="$router.push('labels/import?type=' + labelType)"
        @download="download"
      />
      <v-btn
        v-if="!canOnlyAdd"
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-card-title>
    <label-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
      :disable-edit="canOnlyAdd"
      @edit="editItem"
    />
  </v-card>
</template>

<script lang="ts">
import { mapGetters } from 'vuex'
import Vue from 'vue'
import ActionMenu from '@/components/label/ActionMenu.vue'
import FormDelete from '@/components/label/FormDelete.vue'
import LabelList from '@/components/label/LabelList.vue'
import { LabelDTO } from '~/services/application/label/labelData'
import { MemberItem } from '~/domain/models/member/member'

export default Vue.extend({
  components: {
    ActionMenu,
    FormDelete,
    LabelList
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, app, store }) {
    if (/^\d+$/.test(params.id)) {
      const project = store.getters['projects/project']
      if (!project.canDefineLabel) {
        return false
      }
      return app.$repositories.member.fetchMyRole(params.id).then((member: MemberItem) => {
        if (member.isProjectAdmin) {
          return true
        }
        return project.allowMemberToCreateLabelType
      })
    }
    return false
  },

  data() {
    return {
      dialogDelete: false,
      items: [] as LabelDTO[],
      selected: [] as LabelDTO[],
      isLoading: false,
      tab: 0,
      member: {} as MemberItem
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),

    canOnlyAdd(): boolean {
      if (this.member.isProjectAdmin) {
        return false
      }
      return this.project.allowMemberToCreateLabelType
    },

    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

    hasMultiType(): boolean {
      if ('projectType' in this.project) {
        return this.isIntentDetectionAndSlotFilling || !!this.project.useRelation
      } else {
        return false
      }
    },

    isIntentDetectionAndSlotFilling(): boolean {
      return this.project.projectType === 'IntentDetectionAndSlotFilling'
    },

    labelType(): string {
      if (this.hasMultiType) {
        if (this.isIntentDetectionAndSlotFilling) {
          return ['category', 'span'][this.tab!]
        } else {
          return ['span', 'relation'][this.tab!]
        }
      } else if (this.project.canDefineCategory) {
        return 'category'
      } else {
        return 'span'
      }
    },

    service(): any {
      if (!('projectType' in this.project)) {
        return
      }
      if (this.hasMultiType) {
        if (this.isIntentDetectionAndSlotFilling) {
          return [this.$services.categoryType, this.$services.spanType][this.tab!]
        } else {
          return [this.$services.spanType, this.$services.relationType][this.tab!]
        }
      } else if (this.project.canDefineCategory) {
        return this.$services.categoryType
      } else {
        return this.$services.spanType
      }
    }
  },

  watch: {
    tab() {
      this.list()
    }
  },

  async created() {
    this.member = await this.$repositories.member.fetchMyRole(this.projectId)
    await this.list()
  },

  methods: {
    async list() {
      this.isLoading = true
      this.items = await this.service.list(this.projectId)
      this.isLoading = false
    },

    async remove() {
      await this.service.bulkDelete(this.projectId, this.selected)
      this.list()
      this.dialogDelete = false
      this.selected = []
    },

    async download() {
      await this.service.export(this.projectId)
    },

    editItem(item: LabelDTO) {
      this.$router.push(`labels/${item.id}/edit?type=${this.labelType}`)
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
