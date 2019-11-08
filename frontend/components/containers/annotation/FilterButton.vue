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
      <v-list-item-group v-model="selected">
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
import { mapMutations, mapActions, mapGetters } from 'vuex'
export default {
  data() {
    return {
      selected: 0,
      items: [
        { title: 'All', param: '' },
        { title: 'Done', param: 'false' },
        { title: 'Undone', param: 'true' }
      ]
    }
  },

  computed: {
    ...mapGetters('projects', ['getFilterOption'])
  },

  watch: {
    selected() {
      this.initSearchOptions()
      this.updateSearchOptions({
        isChecked: this.items[this.selected].param,
        filterName: this.getFilterOption
      })
      this.getDocumentList({
        projectId: this.$route.params.id
      })
      this.setCurrent(0)
      const checkpoint = {}
      checkpoint[this.$route.params.id] = this.page
      localStorage.setItem('checkpoint', JSON.stringify(checkpoint))
    }
  },

  methods: {
    ...mapActions('documents', ['getDocumentList']),
    ...mapMutations('documents', ['setCurrent', 'updateSearchOptions', 'initSearchOptions'])
  }
}
</script>
