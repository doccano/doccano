<template>
  <v-card>
    <v-tabs v-model="tab">
      <v-tabs-slider color="primary" />
      <v-tab href="#tab-project" class="text-capitalize"> Project </v-tab>
      <v-tab href="#tab-auto-labeling" class="text-capitalize"> Auto Labeling </v-tab>
    </v-tabs>
    <v-divider />

    <v-tabs-items v-model="tab">
      <v-tab-item value="tab-project">
        <form-update />
      </v-tab-item>
      <v-tab-item value="tab-auto-labeling">
        <config-list />
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import FormUpdate from '@/components/project/FormUpdate.vue'
import ConfigList from '@/components/configAutoLabeling/ConfigList.vue'

export default Vue.extend({
  components: {
    ConfigList,
    FormUpdate
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      tab: null
    }
  }
})
</script>
