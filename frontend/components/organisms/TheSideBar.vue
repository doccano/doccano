<template>
  <v-list dense>
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
  data: () => ({
    items: [
      { icon: 'mdi-database', text: 'Dataset', link: 'dataset' },
      { icon: 'label', text: 'Labels', link: 'labels' },
      { icon: 'person', text: 'Members', link: 'members' },
      { divider: true },
      { icon: 'backup', text: 'Import', link: 'upload' },
      { icon: 'archive', text: 'Export', link: 'download' },
      { divider: true },
      { icon: 'settings', text: 'Guideline', link: 'guideline' },
      { icon: 'chat_bubble', text: 'Statistics', link: 'statistics' }
    ]
  })
}
</script>
