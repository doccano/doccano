<template>
  <v-menu>
    <template v-slot:activator="{ on: menu }">
      <v-tooltip bottom>
        <template v-slot:activator="{ on: tooltip }">
          <v-btn
            class="text-capitalize ps-1 pe-1"
            min-width="36"
            outlined
            v-on="{ ...tooltip, ...menu }"
          >
            <v-icon>
              mdi-filter
            </v-icon>
          </v-btn>
        </template>
        <span>Select a filter</span>
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
        { title: 'All', param: '' },
        { title: 'Done', param: 'false' },
        { title: 'Undone', param: 'true' }
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
        this.$emit('input', this.items[value].param)
      }
    }
  }
}
</script>
