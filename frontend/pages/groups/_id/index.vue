<template>
  <v-card>
    <v-card-title>
      <v-btn
        icon
        class="mr-2"
        @click="goBack"
      >
        <v-icon>{{ mdiArrowLeft }}</v-icon>
      </v-btn>
      {{ group.name }}
      <v-spacer></v-spacer>
      <v-btn
        v-if="isStaff"
        class="text-capitalize ms-2"
        color="primary"
        outlined
        @click="dialogUpdate = true"
      >
        {{ $t('generic.edit') }}
      </v-btn>
      <v-dialog v-model="dialogUpdate" max-width="800px">
        <form-update
          :group="group"
          @cancel="dialogUpdate = false"
          @updated="handleUpdated"
        />
      </v-dialog>
    </v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" sm="6">
          <v-card outlined>
            <v-card-title>{{ $t('group.details') }}</v-card-title>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>{{ $t('group.id') }}</v-list-item-title>
                <v-list-item-subtitle>{{ group.id }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>{{ $t('group.name') }}</v-list-item-title>
                <v-list-item-subtitle>{{ group.name }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6">
          <v-card outlined>
            <v-card-title>{{ $t('group.permissions') }}</v-card-title>
            <v-card-text v-if="isLoading">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </v-card-text>
            <v-card-text v-else>
              <v-chip
                v-for="(permission, id) in permissionsToDisplay"
                :key="id"
                color="primary"
                small
                class="ma-1"
              >
                {{ permission.name }}
              </v-chip>
              <div v-if="!permissionsToDisplay || Object.keys(permissionsToDisplay).length === 0" class="text-center grey--text">
                {{ $t('group.noPermissions') }}
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import { mdiArrowLeft } from '@mdi/js'
import { GroupDetails, Permission } from '@/domain/models/group/group'
import FormUpdate from '@/components/groups/FormUpdate.vue'

export default Vue.extend({
  components: {
    FormUpdate
  },

  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      group: {} as GroupDetails,
      isLoading: false,
      dialogUpdate: false,
      permissions: [] as Permission[],
      mdiArrowLeft
    }
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    
    permissionsToDisplay() {
      return this.group.permission_names || {}
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      const id = Number(this.$route.params.id)
      this.group = await this.$services.group.getGroup(id)
    } catch (e) {
      this.$store.dispatch('notification/setNotification', {
        color: 'error',
        text: 'Failed to load group details'
      })
    } finally {
      this.isLoading = false
    }
  },

  methods: {
    goBack() {
      this.$router.push(this.localePath('/groups'))
    },

    handleUpdated() {
      this.dialogUpdate = false
      this.$fetch()
      this.$store.dispatch('notification/setNotification', {
        color: 'success',
        text: 'Group updated successfully'
      })
    }
  }
})
</script>
