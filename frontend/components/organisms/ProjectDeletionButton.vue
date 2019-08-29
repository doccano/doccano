<template>
  <div>
    <v-btn
      class="mb-2 ml-2 text-capitalize"
      outlined
      :disabled="selected.length === 0"
      @click="dialog=true"
    >
      Remove
    </v-btn>

    <v-dialog
      v-model="dialog"
      width="800px"
    >
      <base-card
        title="Delete Project"
        button="Yes, delete"
        :disabled="disabled"
        @cancel="dialog=false"
        @agree="deleteProject"
      >
        <template #content>
          Are you sure you want to remove these projects?
          <v-list dense>
            <v-list-item v-for="(item, i) in selected" :key="i">
              <v-list-item-content>
                <v-list-item-title>{{ item.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </template>
      </base-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import BaseCard from '@/components/BaseCard'

export default {
  components: {
    BaseCard
  },
  data: () => ({
    dialog: false,
    disabled: false
  }),

  computed: {
    ...mapState('ProjectList', ['projects', 'selected'])
  },

  methods: {
    deleteProject() {
      this.$store.dispatch('ProjectList/deleteProject')
      // this.$emit('remove')
      this.dialog = false
    }
  }
}
</script>
