<template>
  <v-card>
    <v-card-title>
      {{ $t('dataset.importDataTitle') }}
    </v-card-title>
    <v-card-text>
      <v-overlay :value="isImporting">
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
      <v-select
        v-model="selected"
        :items="catalog"
        item-text="displayName"
        label="File format"
        outlined
      />
      <v-form v-model="valid">
        <v-text-field
          v-for="(item, key) in textFields"
          :key="key"
          v-model="option[key]"
          :label="item.title"
          :rules="requiredRules"
          outlined
        />
        <v-select
          v-for="(val, key) in selectFields"
          :key="key"
          v-model="option[key]"
          :items="val.enum"
          :label="val.title"
          outlined
        >
          <template #selection="{ item }">
            {{ toVisualize(item) }}
          </template>
          <template #item="{ item }">
            {{ toVisualize(item) }}
          </template>
        </v-select>
      </v-form>
      <v-sheet
        v-if="selected"
        :dark="!$vuetify.theme.dark"
        :light="$vuetify.theme.dark"
        class="mb-5 pa-5"
      >
        <pre>{{ example }}</pre>
      </v-sheet>
      <div v-if="selected === 'JSONL(Relation)'">
        <p class="body-1">For readability, the above format can be displayed as follows:</p>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ JSON.stringify(JSON.parse(example.replaceAll("'", '"')), null, 4) }}</pre>
        </v-sheet>
      </div>
      <file-pond
        v-if="selected && acceptedFileTypes !== '*'"
        ref="pond"
        chunk-uploads="true"
        label-idle="Drop files here..."
        :allow-multiple="true"
        :accepted-file-types="acceptedFileTypes"
        :server="server"
        :files="myFiles"
        @processfile="handleFilePondProcessFile"
        @removefile="handleFilePondRemoveFile"
      />
      <file-pond
        v-if="selected && acceptedFileTypes === '*'"
        ref="pond"
        chunk-uploads="true"
        label-idle="Drop files here..."
        :allow-multiple="true"
        :server="server"
        :files="myFiles"
        @processfile="handleFilePondProcessFile"
        @removefile="handleFilePondRemoveFile"
      />
      <v-data-table
        v-if="errors.length > 0"
        :headers="headers"
        :items="errors"
        class="elevation-1"
      ></v-data-table>
    </v-card-text>
    <v-card-actions>
      <v-btn class="text-capitalize ms-2 primary" :disabled="isDisabled" @click="importDataset">
        {{ $t('generic.import') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type'
import 'filepond/dist/filepond.min.css'
import Cookies from 'js-cookie'
import vueFilePond from 'vue-filepond'
const FilePond = vueFilePond(FilePondPluginFileValidateType)

export default {
  components: {
    FilePond
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      catalog: [],
      selected: null,
      myFiles: [],
      option: { column_data: '', column_label: '', delimiter: '' },
      taskId: null,
      polling: null,
      errors: [],
      headers: [
        { text: 'Filename', value: 'filename' },
        { text: 'Line', value: 'line' },
        { text: 'Message', value: 'message' }
      ],
      requiredRules: [(v) => !!v || 'Field value is required'],
      server: {
        url: '/v1/fp',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        process: {
          url: '/process/',
          method: 'POST'
        },
        patch: '/patch/',
        revert: '/revert/',
        restore: '/restore/',
        load: '/load/',
        fetch: '/fetch/'
      },
      uploadedFiles: [],
      valid: false,
      isImporting: false
    }
  },

  computed: {
    isDisabled() {
      return this.uploadedFiles.length === 0 || this.taskId !== null || !this.valid
    },
    properties() {
      const item = this.catalog.find((item) => item.displayName === this.selected)
      if (item) {
        return item.properties
      } else {
        return {}
      }
    },
    textFields() {
      const asArray = Object.entries(this.properties)
      const textFields = asArray.filter(([_, value]) => !('enum' in value))
      return Object.fromEntries(textFields)
    },
    selectFields() {
      const asArray = Object.entries(this.properties)
      const textFields = asArray.filter(([_, value]) => 'enum' in value)
      return Object.fromEntries(textFields)
    },
    acceptedFileTypes() {
      const item = this.catalog.find((item) => item.displayName === this.selected)
      if (item) {
        return item.acceptTypes
      } else {
        return ''
      }
    },
    example() {
      const item = this.catalog.find((item) => item.displayName === this.selected)
      if (item) {
        const column_data = 'column_data'
        const column_label = 'column_label'
        if (column_data in this.option && column_label in this.option) {
          return item.example
            .replaceAll(column_data, this.option[column_data])
            .replaceAll(column_label, this.option[column_label])
            .trim()
        } else {
          return item.example.trim()
        }
      } else {
        return ''
      }
    }
  },

  watch: {
    selected() {
      const item = this.catalog.find((item) => item.displayName === this.selected)
      for (const [key, value] of Object.entries(item.properties)) {
        this.option[key] = value.default
      }
      this.myFiles = []
      for (const file of this.uploadedFiles) {
        this.$repositories.parse.revert(file.serverId)
      }
      this.uploadedFiles = []
      this.errors = []
    }
  },

  async created() {
    this.catalog = await this.$repositories.catalog.list(this.$route.params.id)
    this.pollData()
  },

  beforeDestroy() {
    clearInterval(this.polling)
  },

  methods: {
    handleFilePondProcessFile(error, file) {
      console.log(error)
      this.uploadedFiles.push(file)
      this.$nextTick()
    },
    handleFilePondRemoveFile(error, file) {
      console.log(error)
      const index = this.uploadedFiles.findIndex((item) => item.id === file.id)
      if (index > -1) {
        this.uploadedFiles.splice(index, 1)
        this.$nextTick()
      }
    },
    async importDataset() {
      this.isImporting = true
      const item = this.catalog.find((item) => item.displayName === this.selected)
      this.taskId = await this.$repositories.parse.analyze(
        this.$route.params.id,
        item.name,
        item.taskId,
        this.uploadedFiles.map((item) => item.serverId),
        this.option
      )
    },
    pollData() {
      this.polling = setInterval(async () => {
        if (this.taskId) {
          const res = await this.$repositories.taskStatus.get(this.taskId)
          if (res.ready) {
            this.taskId = null
            this.errors = res.result.error
            this.myFiles = []
            this.uploadedFiles = []
            this.isImporting = false
            if (this.errors.length === 0) {
              this.$router.push(`/projects/${this.$route.params.id}/dataset`)
            }
          }
        }
      }, 3000)
    },
    toVisualize(text) {
      if (text === '\t') {
        return 'Tab'
      } else if (text === ' ') {
        return 'Space'
      } else if (text === '') {
        return 'None'
      } else {
        return text
      }
    }
  }
}
</script>
