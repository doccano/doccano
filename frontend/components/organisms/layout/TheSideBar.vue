<template>
  <v-list dense>
    <v-btn
      color="ms-4 my-1 mb-2 primary text-capitalize"
      nuxt
      @click="toLabeling"
    >
      <v-icon left>
        mdi-play-circle-outline
      </v-icon>
      Start annotation
    </v-btn>
    <v-list-item-group
      v-model="selected"
      mandatory
    >
      <v-list-item
        v-for="(item, i) in filteredItems"
        :key="i"
        @click="$router.push(`/projects/${$route.params.id}/${item.link}`)"
      >
        <v-list-item-action>
          <v-icon>
            {{ item.icon }}
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            {{ item.text }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    link: {
      type: String,
      default: '',
      required: true
    },
    role: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  data() {
    return {
      selected: 0,
      items: [
        { icon: 'mdi-home', text: 'Home', link: '', adminOnly: false },
        { icon: 'mdi-database', text: 'Dataset', link: 'dataset', adminOnly: true },
        { icon: 'label', text: 'Labels', link: 'labels', adminOnly: true },
        { icon: 'person', text: 'Members', link: 'members', adminOnly: true },
        { icon: 'mdi-book-open-outline', text: 'Guideline', link: 'guideline', adminOnly: true },
        { icon: 'mdi-chart-bar', text: 'Statistics', link: 'statistics', adminOnly: true }
      ]
    }
  },

  computed: {
    ...mapGetters('projects', ['loadSearchOptions']),
    filteredItems() {
      return this.items.filter(item => this.isVisible(item))
    }
  },

  methods: {
    isVisible(item) {
      return !item.adminOnly || this.role.is_project_admin
    },
    toLabeling() {
      this.$router.push({
        path: `/projects/${this.$route.params.id}/${this.link}`,
        query: this.loadSearchOptions
      })
    }
  }
}
</script>
