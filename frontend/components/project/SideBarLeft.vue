<template>
  <v-list
    dense
    class=""
  >
    <v-list-item>
      <v-btn rounded color="white">
        <v-icon left>
          mdi-plus
        </v-icon> Start Labeling
      </v-btn>
    </v-list-item>
    <template v-for="(item, i) in items">
      <v-layout
        v-if="item.heading"
        :key="i"
        align-center
      >
        <v-flex xs6>
          <v-subheader v-if="item.heading">
            {{ item.heading }}
          </v-subheader>
        </v-flex>
        <v-flex
          xs6
          class="text-right"
        >
          <v-btn
            small
            text
          >
            edit
          </v-btn>
        </v-flex>
      </v-layout>
      <v-divider
        v-else-if="item.divider"
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
  data: () => ({
    items: [
      // { icon: 'lightbulb_outline', text: 'Start Labeling' },
      { divider: true },
      { icon: 'mdi-database', text: 'Dataset', link: 'dataset' },
      { icon: 'person', text: 'User', link: 'users' },
      { icon: 'label', text: 'Label', link: 'labels' },
      { divider: true },
      // { heading: 'Labels' },
      // { icon: 'add', text: 'Create new label', link: 'labels' },
      // { divider: true },
      { icon: 'backup', text: 'Import', link: 'upload' },
      { icon: 'archive', text: 'Export', link: 'download' },
      { divider: true },
      { icon: 'settings', text: 'Guideline', link: 'guideline' },
      { icon: 'chat_bubble', text: 'Statistics', link: 'statistics' },
      { icon: 'help', text: 'Help', link: 'help' }
      // { icon: 'keyboard', text: 'Keyboard shortcuts' }
    ]
  })
}
</script>
