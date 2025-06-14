<template>
  <base-card
    :title="$t('Edit User')"
    :agree-text="$t('generic.save')"
    :cancel-text="$t('generic.cancel')"
    @agree="submit"
    @cancel="$emit('cancel')"
  >
    <template #content>
      <v-form ref="form" v-model="valid">
        <v-text-field
          v-model="formData.username"
          :label="$t('Username')"
          :rules="[rules.required]"
        />
        <v-text-field v-model="formData.first_name" :label="$t('First Name')" />
        <v-text-field v-model="formData.last_name" :label="$t('Last Name')" />
        <v-text-field
          v-model="formData.email"
          :label="$t('Email')"
          :rules="[rules.required]"
          type="email"
        />
        <v-text-field
          v-model="formData.password"
          :label="$t('Password (leave blank to keep unchanged)')"
          type="password"
          :rules="[rules.password]"
        />
        <!-- Campos booleanos com checkboxes -->
        <v-checkbox v-model="formData.isSuperUser" :label="$t('Superuser')" />
        <v-checkbox v-model="formData.isStaff" :label="$t('Staff')" />
      </v-form>
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { UserDTO } from '~/services/application/user/userData'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    user: {
      type: Object as () => UserDTO,
      required: true
    }
  },

  data() {
    return {
      formData: {
        id: this.user.id,
        username: this.user.username,
        first_name: this.user.first_name,
        last_name: this.user.last_name,
        email: this.user.email,
        password: '',
        isSuperUser: this.user.isSuperUser,
        isStaff: this.user.isStaff
      },
      valid: false,
      rules: {
        required: (v: string) => !!v || 'Required',
        password: (v: string) => {
          if (!v) return true
          return (
            /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/.test(v) ||
            'A palavra-passe deve ter pelo menos 8 caracteres e conter letras e números.'
          )
        }
      }
    }
  },

  methods: {
    submit() {
      const form = this.$refs.form as Vue & { validate: () => boolean }
      if (!form.validate()) return

      const updatedUser: any = {
        id: this.formData.id,
        username: this.formData.username,
        first_name: this.formData.first_name,
        last_name: this.formData.last_name,
        email: this.formData.email,
        isSuperUser: this.formData.isSuperUser,
        isStaff: this.formData.isStaff
      }

      if (this.formData.password) {
        updatedUser.password = this.formData.password
      }

      this.$emit('confirmEdit', updatedUser)
    }
  }
})
</script>
