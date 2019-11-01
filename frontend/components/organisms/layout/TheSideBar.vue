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
      <v-divider
        v-if="item.divider"
        :key="i"
        dark
        class="my-4"
      />
      <v-list-item
        v-else
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
    }
  },

  data() {
    return {
      items: [
        { icon: 'mdi-home', text: 'Home', link: '' },
        { icon: 'mdi-database', text: 'Dataset', link: 'dataset' },
        { icon: 'label', text: 'Labels', link: 'labels' },
        { icon: 'person', text: 'Members', link: 'members' },
        { icon: 'mdi-book-open-outline', text: 'Guideline', link: 'guideline' },
        { icon: 'mdi-chart-bar', text: 'Statistics', link: 'statistics' }
      ]
    }
  },

  computed: {
    to() {
      return `/projects/${this.$route.params.id}/${this.link}`
    }
  }
}
</script>
