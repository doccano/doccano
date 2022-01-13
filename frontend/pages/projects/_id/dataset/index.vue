<template>
  <v-card>
    <v-card-title v-if="isProjectAdmin">
      <action-menu
        @upload="upload"
        @download="dialogDownload=true"
      />
      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete=true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-spacer />
      <v-btn
        :disabled="!item.count"
        class="text-capitalize"
        color="error"
        @click="dialogDeleteAll=true"
      >
        {{ $t('generic.deleteAll') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete
          :selected="selected"
          :item-key="itemKey"
          @cancel="dialogDelete=false"
          @remove="remove"
        />
      </v-dialog>
      <v-dialog v-model="dialogDeleteAll">
        <form-delete-bulk
          @cancel="dialogDeleteAll=false"
          @remove="removeAll"
        />
      </v-dialog>
      <v-dialog v-model="dialogDownload">
        <form-download
          @cancel="dialogDownload=false"
        />
      </v-dialog>
    </v-card-title>
    <image-list
      v-if="isImageTask"
      v-model="selected"
      :items="item.items"
      :is-loading="isLoading"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
    />
    <audio-list
      v-else-if="isAudioTask"
      v-model="selected"
      :items="item.items"
      :is-loading="isLoading"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
    />
    <document-list
      v-else
      v-model="selected"
      :items="item.items"
      :is-loading="isLoading"
      :total="item.count"
      @update:query="updateQuery"
      @click:labeling="movePage"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import _ from 'lodash'
import DocumentList from '@/components/example/DocumentList.vue'
import FormDelete from '@/components/example/FormDelete.vue'
import FormDeleteBulk from '@/components/example/FormDeleteBulk.vue'
import FormDownload from '@/components/example/FormDownload.vue'
import ImageList from '~/components/example/ImageList.vue'
import AudioList from '~/components/example/AudioList.vue'
import { ExampleListDTO, ExampleDTO } from '~/services/application/example/exampleData'
import ActionMenu from '~/components/example/ActionMenu.vue'
import { ProjectDTO } from '~/services/application/project/projectData'

export default Vue.extend({

  components: {
    ActionMenu,
    AudioList,
    DocumentList,
    ImageList,
    FormDelete,
    FormDeleteBulk,
    FormDownload,
  },

  layout: 'project',

  validate({ params, query }) {
    // @ts-ignore
    return /^\d+$/.test(params.id) && /^\d+|$/.test(query.limit) && /^\d+|$/.test(query.offset)
  },

  data() {
    return {
      dialogDelete: false,
      dialogDeleteAll: false,
      dialogDownload: false,
      project: {} as ProjectDTO,
      item: {} as ExampleListDTO,
      selected: [] as ExampleDTO[],
      isLoading: false,
      isProjectAdmin: false
    }
  },

  async fetch() {
    this.isLoading = true
    this.item = await this.$services.example.list(this.projectId, this.$route.query)
    this.isLoading = false
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
    },
    isImageTask(): boolean {
      return this.project.projectType === 'ImageClassification'
    },
    isAudioTask(): boolean {
      return this.project.projectType === 'Speech2text'
    },
    itemKey(): string {
      if (this.isImageTask || this.isAudioTask) {
        return 'filename'
      } else {
        return 'text'
      }
    },
    ...mapGetters('auth', ['getUserId'])
  },

  watch: {
    '$route.query': _.debounce(function() {
        // @ts-ignore
        this.$fetch()
      }, 1000
    ),
  },

  async created() {
    this.project = await this.$services.project.findById(this.projectId)
    this.isProjectAdmin = await this.$services.member.isProjectAdmin(this.projectId, this.getUserId)
  },

  methods: {
    async remove() {
      await this.$services.example.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },
    async removeAll() {
      await this.$services.example.bulkDelete(this.projectId, [])
      this.$fetch()
      this.dialogDeleteAll = false
      this.selected = []
    },
    upload() {
      this.$router.push(`/projects/${this.projectId}/upload`)
    },
    updateQuery(query: object) {
      this.$router.push(query)
    },
    movePage(query: object) {
      this.updateQuery({
        path: this.localePath(this.project.pageLink),
        query
      })
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
