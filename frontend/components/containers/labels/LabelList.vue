<template>
  <v-data-table
    :value="selected"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="loading"
    loading-text="Loading... Please wait"
    item-key="id"
    show-select
    @input="updateSelected"
  >
    <template v-slot:top>
      <v-text-field
        v-model="search"
        prepend-inner-icon="search"
        label="Search"
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
            :rules="labelNameRules"
            label="Edit"
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
            :items="keys"
            label="Key"
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
            :value="item.backgroundColor"
            :rules="colorRules"
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
import { mapState, mapActions, mapMutations } from 'vuex'
import { colorRules, labelNameRules } from '@/rules/index'
import { idealColor } from '~/plugins/utils'

export default {
  data() {
    return {
      search: '',
      headers: [
        {
          text: 'Name',
          align: 'left',
          value: 'text'
        },
        {
          text: 'Shortkey',
          value: 'suffix_key'
        },
        {
          text: 'Color',
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

    keys() {
      return 'abcdefghijklmnopqrstuvwxyz'.split('')
    }
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

    textColor(backgroundColor) {
      return idealColor(backgroundColor)
    }
  }
}
</script>
