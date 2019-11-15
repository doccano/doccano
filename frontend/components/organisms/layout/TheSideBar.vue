<template>
  <v-list dense>
    <v-btn
      color="ms-4 my-1 mb-2 primary text-capitalize"
      :to="to"
      nuxt
    >
      <v-icon left>
        mdi-play-circle-outline
      </v-icon>
      Start annotation
    </v-btn>
    <template v-for="(item, i) in items">
      <v-list-item
        v-if="isVisible(item)"
        :key="i"
        @click="$router.push('/projects/' + $route.params.id + '/' + item.link)"
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
    </template>
  </v-list>
</template>

<script>
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
    to() {
      return `/projects/${this.$route.params.id}/${this.link}`
    }
  },

  methods: {
    isVisible(item) {
      return !item.adminOnly || this.role.is_project_admin
    }
  }
}
</script>
