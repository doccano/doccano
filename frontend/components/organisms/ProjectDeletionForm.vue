<template>
  <base-card
    title="Delete Project"
    agree-text="Yes, delete"
    cancel-text="Cancel"
    @agree="deleteProject"
    @cancel="cancel"
  >
    <template #content>
      Are you sure you want to delete these projects?
      <v-list dense>
        <v-list-item v-for="(item, i) in selected" :key="i">
          <v-list-item-content>
            <v-list-item-title>{{ item.name }}</v-list-item-title>
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
    deleteProject() {
      this.$emit('delete')
    }
  }
}
</script>
