<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="loading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      'showFirstLastPage': true,
      'items-per-page-options': [5, 10, 15, $t('generic.all')],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="updateSelected"
  >
    <template v-slot:top>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template v-slot:item.text="{ item }">
      <v-edit-dialog>
        {{ item.text }}
        <template v-slot:input>
          <v-text-field
            :value="item.text"
            :rules="labelNameRules($t('rules.labelNameRules'))"
            :label="$t('generic.edit')"
            single-line
            @change="handleUpdateLabel({ id: item.id, text: $event })"
          />
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.suffix_key="{ item }">
      <v-edit-dialog>
        <div>{{ item.suffix_key }}</div>
        <template v-slot:input>
          <v-select
            :value="item.suffix_key"
            :items="availableShortkeys(item.suffix_key)"
            :label="$t('annotation.key')"
            @change="handleUpdateLabel({ id: item.id, suffix_key: $event })"
          />
        </template>
      </v-edit-dialog>
    </template>
    <template v-slot:item.background_color="{ item }">
      <v-edit-dialog>
        <v-chip
          :color="item.background_color"
          :text-color="textColor(item.background_color)"
          dark
        >
          {{ item.background_color }}
        </v-chip>
        <template v-slot:input>
          <v-color-picker
            :value="item.background_color"
            :rules="colorRules($t('rules.colorRules'))"
            show-swatches
            hide-mode-switch
            width="800"
            mode="hexa"
            class="ma-2"
            @update:color="handleUpdateLabel({ id:item.id, background_color: $event.hex })"
          />
        </template>
      </v-edit-dialog>
    </template>
  </v-data-table>
</template>

<script>
import { mapGetters, mapState, mapActions, mapMutations } from 'vuex'
import { colorRules, labelNameRules } from '@/rules/index'
import { idealColor } from '~/plugins/utils'

export default {
  data() {
    return {
      search: '',
      headers: [
        {
          text: this.$t('generic.name'),
          align: 'left',
          value: 'text'
        },
        {
          text: this.$t('labels.shortkey'),
          value: 'suffix_key'
        },
        {
          text: this.$t('labels.color'),
          sortable: false,
          value: 'background_color'
        }
      ],
      colorRules,
      labelNameRules
    }
  },

  computed: {
    ...mapState('labels', ['items', 'selected', 'loading']),
    ...mapGetters('labels', ['shortkeys'])
  },

  created() {
    this.getLabelList({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('labels', ['getLabelList', 'updateLabel']),
    ...mapMutations('labels', ['updateSelected']),

    handleUpdateLabel(payload) {
      const data = {
        projectId: this.$route.params.id,
        ...payload
      }
      this.updateLabel(data)
    },

    availableShortkeys(suffixKey) {
      const usedKeys = this.items.map(item => item.suffix_key)
      const unusedKeys = this.shortkeys.filter(item => item === suffixKey || !usedKeys.includes(item))
      return unusedKeys
    },

    textColor(backgroundColor) {
      return idealColor(backgroundColor)
    }
  }
}
</script>
