<template>
  <base-card title="Keyboard Shortcut" :cancel-text="$t('generic.close')" @cancel="close">
    <template #content>
      <v-simple-table>
        <template #default>
          <thead>
            <tr>
              <th class="text-left">Action</th>
              <th class="text-left">Key</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.name">
              <td>{{ item.name }}</td>
              <td>
                <v-chip
                  v-for="key in item.key"
                  :key="key"
                  color="grey darken-3 white--text"
                  class="ma-1"
                  label
                  small
                  >{{ key }}</v-chip
                >
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/utils/BaseCard'

export default {
  components: {
    BaseCard
  },

  data() {
    return {
      items: [
        {
          name: 'Jump to the first data',
          key: ['shift', '←']
        },
        {
          name: 'Jump to the last data',
          key: ['shift', '→']
        },
        {
          name: 'Move to the previous data',
          key: ['←']
        },
        {
          name: 'Move to the next data',
          key: ['→']
        },
        {
          name: 'Confirm the data',
          key: ['enter']
        }
      ]
    }
  },

  methods: {
    close() {
      this.$emit('click:close')
    }
  }
}
</script>
