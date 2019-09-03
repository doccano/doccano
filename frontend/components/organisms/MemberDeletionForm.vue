<template>
  <base-card
    title="Remove Member"
    agree-text="Yes, remove"
    cancel-text="Cancel"
    @agree="removeMember"
    @cancel="cancel"
  >
    <template #content>
      Are you sure you want to remove these members?
      <v-list dense>
        <v-list-item v-for="(item, i) in selected" :key="i">
          <v-list-item-content>
            <v-list-item-title>{{ item.username }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/molecules/BaseCard'

export default {
  components: {
    BaseCard
  },

  props: {
    selected: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  methods: {
    cancel() {
      this.$emit('close')
    },
    removeMember() {
      this.$emit('remove')
    }
  }
}
</script>
