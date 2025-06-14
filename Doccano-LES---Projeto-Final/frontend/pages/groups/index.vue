<template>
  <v-card>
    <v-card-title>
      <v-btn class="text-capitalize" color="primary" @click.stop="$router.push('groups/add')">
        {{ $t('generic.create') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        outlined
        :disabled="!canDelete"
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-btn
        class="text-capitalize ms-2"
        outlined
        :disabled="selected.length !== 1"
        @click.stop="dialogEdit = true"
      >
        {{ $t('generic.edit') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @remove="handleDelete" @cancel="dialogDelete = false" />
      </v-dialog>
      <v-dialog v-model="dialogEdit">
        <form-edit :user="selected[0]" @confirmEdit="handleEdit" @cancel="dialogEdit = false" />
      </v-dialog>
    </v-card-title>
    <user-list v-model="selected" :items="items" :is-loading="isLoading" />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'

export default Vue.extend({
  components: {},

  layout: 'projects',

  middleware: ['check-auth', 'auth', 'isSuperUser'],

  data() {
    return {
      dialogDelete: false,
      items: [],
      selected: [],
      dialogEdit: false,
      isLoading: false,
      tab: 0,
      drawerLeft: null
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff', 'isSuperUser'])
  },

  mounted() {},

  methods: {}
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
