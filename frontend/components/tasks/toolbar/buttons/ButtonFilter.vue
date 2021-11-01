<template>
  <v-menu>
    <template #activator="{ on: menu }">
      <v-tooltip bottom>
        <template #activator="{ on: tooltip }">
          <v-btn
            icon
            v-on="{ ...tooltip, ...menu }"
          >
            <v-icon>
              mdi-filter
            </v-icon>
          </v-btn>
        </template>
        <span>{{ $t('annotation.selectFilterTooltip') }}</span>
      </v-tooltip>
    </template>
    <v-list>
      <v-list-item-group v-model="selected" mandatory>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
        >
          <v-list-item-icon>
            <v-icon v-if="selected === i">
              mdi-check
            </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              {{ item.title }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  props: {
    value: {
      type: String,
      default: '',
      required: true
    }
  },

  data() {
    return {
      items: [
        { title: this.$t('annotation.filterOption1'), param: '' },
        { title: this.$t('annotation.filterOption2'), param: 'true' },
        { title: this.$t('annotation.filterOption3'), param: 'false' }
      ]
    }
  },

  computed: {
    selected: {
      get() {
        const index = this.items.findIndex(item => item.param === this.value)
        return index === -1 ? 0 : index
      },
      set(value) {
        this.$emit('click:filter', this.items[value].param)
      }
    }
  }
}
</script>
