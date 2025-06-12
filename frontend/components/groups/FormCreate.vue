<template>
  <v-card>
    <v-card-title>{{ $t('group.create') }}</v-card-title>
    <v-card-text>
      <v-container>
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="name"
            :label="$t('group.name')"
            :rules="nameRules"
            required
          />
          <v-card-subtitle>{{ $t('group.permissions') }}</v-card-subtitle>
          <v-progress-circular
            v-if="isLoadingPermissions"
            indeterminate
            color="primary"
            class="my-5"
          ></v-progress-circular>
          <template v-else>
            <v-autocomplete
              v-model="selectedPermissions"
              :items="permissions"
              :item-text="permissionLabel"
              :search-input.sync="permissionsSearch"
              :label="$t('group.selectPermissions')"
              :no-data-text="$t('vuetify.noDataAvailable')"
              chips
              small-chips
              deletable-chips
              multiple
              clearable
              dense
              outlined
              hide-selected
              return-object
            >
              <template #selection="{ item, index }">
                <v-chip
                  v-if="index === 0"
                  small
                  close
                  @click:close="removePermission(item)"
                >
                  <span>{{ permissionLabel(item) }}</span>
                </v-chip>
                <span v-if="index === 1" class="grey--text text-caption">
                  (+{{ selectedPermissions.length - 1 }} {{ $t('generic.more') }})
                </span>
              </template>
              <template #item="{ item }">
                <v-list-item-content>
                  <v-list-item-title>
                    {{ permissionLabel(item) }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ item.codename }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </template>
            </v-autocomplete>
            
            <div v-if="selectedPermissions && selectedPermissions.length > 0" class="mt-4">
              <div class="subtitle-1 mb-2">
                {{ $t('group.selectedPermissions') }} ({{ selectedPermissions.length }})
              </div>
              <div class="selected-permissions-container">
                <v-chip-group column>
                  <v-chip
                    v-for="permission in selectedPermissions"
                    :key="permission.id"
                    small
                    close
                    class="ma-1"
                    @click:close="removePermission(permission)"
                  >
                    {{ permissionLabel(permission) }}
                  </v-chip>
                </v-chip-group>
              </div>
            </div>
          </template>
        </v-form>
      </v-container>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text color="grey" @click="$emit('cancel')">
        {{ $t('generic.cancel') }}
      </v-btn>
      <v-btn
        text
        color="primary"
        :disabled="!valid || isSubmitting"
        @click="create"
      >
        {{ $t('generic.create') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { Permission } from '@/domain/models/group/group'

export default Vue.extend({
  data() {
    return {
      valid: false,
      name: '',
      nameRules: [
        (v: string) => !!v || this.$t('rules.required')
      ],
      isSubmitting: false,
      permissions: [] as Permission[],
      selectedPermissions: [] as Permission[],
      isLoadingPermissions: false,
      permissionsSearch: '',
      filteredPermissions: [] as Permission[]
    }
  },

  watch: {
    permissionsSearch(_val) {
      // When using v-autocomplete with server-side filtering, 
      // we could implement additional filtering here if needed
    }
  },

  created() {
    // Ensure selectedPermissions is initialized as an empty array
    this.selectedPermissions = []
  },

  async mounted() {
    await this.fetchPermissions()
  },

  methods: {
    permissionLabel(item: Permission): string {
      return item && (item.label || item.name) || ''
    },
    
    removePermission(permission: Permission) {
      if (!this.selectedPermissions) {
        this.selectedPermissions = []
        return
      }
      this.selectedPermissions = this.selectedPermissions.filter(p => p.id !== permission.id)
    },
    
    async fetchPermissions() {
      this.isLoadingPermissions = true
      try {
        // Fetch all permissions - could be paginated if there are too many
        const response = await this.$services.group.listPermissions('limit=1000')
        this.permissions = response.results
      } catch (error) {
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Failed to load permissions'
        })
      } finally {
        this.isLoadingPermissions = false
      }
    },

    async create() {
      if (!(this.$refs.form as any).validate()) {
        return
      }
      this.isSubmitting = true
      try {
        // Ensure we always have an array of permission IDs
        const permissionIds = Array.isArray(this.selectedPermissions) 
          ? this.selectedPermissions.map(p => p.id) 
          : [];

        // Log for debugging
        console.log('Sending permissions:', permissionIds)
        
        await this.$services.group.createGroup({
          name: this.name,
          permissions: permissionIds
        })
        this.$emit('created')
      } catch (error) {
        console.error('Create group error:', error)
        this.$store.dispatch('notification/setNotification', {
          color: 'error',
          text: 'Failed to create group'
        })
      } finally {
        this.isSubmitting = false
      }
    }
  }
})
</script>

<style lang="scss" scoped>
.v-autocomplete {
  margin-bottom: 10px;
}

.selected-permissions-container {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 8px;
  background-color: #fafafa;
}
</style>
