<template>
  <v-list dense>
    <v-list-item-group :value="selected" mandatory>
      <v-list-item
        v-for="(item, i) in filteredItems"
        :key="i"
        @click="$router.push(localePath(`/${item.link}`))"
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
import { mdiDeveloperBoard, mdiAccount, mdiAccountGroup } from '@mdi/js'

export default {
  data() {
    return {
      selected: 1
    }
  },

  computed: {
    filteredItems() {
      return [
        { icon: mdiDeveloperBoard, text: 'Projects', link: 'projects' },
        { icon: mdiAccount, text: 'Users', link: 'users' },
        { icon: mdiAccountGroup, text: 'Groups', link: 'groups' }
      ]
    }
  }
}
</script>
