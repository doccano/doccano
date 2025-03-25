<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>{{ $t('generic.create') }} {{ $t('user.user') }}</v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="form.username"
            :label="$t('user.username')"
            :rules="[rules.required]"
            required
          />
          <v-text-field
            v-model="form.email"
            :label="$t('user.email')"
            :rules="[rules.required, rules.email]"
            type="email"
            required
          />
          <v-text-field
            v-model="form.password1"
            :label="$t('user.password')"
            :rules="[rules.required, rules.min]"
            type="password"
            required
          />
          <v-text-field
            v-model="form.password2"
            :label="$t('user.confirmPassword')"
            :rules="[rules.required, rules.match]"
            type="password"
            required
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="close">{{ $t('generic.cancel') }}</v-btn>
        <v-btn
          :disabled="!valid"
          color="primary"
          @click="submit"
        >
          {{ $t('generic.save') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      dialog: false,
      valid: false,
      form: {
        username: '',
        email: '',
        password1: '',
        password2: ''
      },
      rules: {
        required: (v: string) => !!v || this.$t('rules.required'),
        email: (v: string) => /.+@.+\..+/.test(v) || this.$t('rules.email'),
        min: (v: string) => v.length >= 8 || this.$t('rules.min', { min: 8 }),
        match: (v: string) => v === this.form.password1 || this.$t('rules.passwordMatch')
      }
    }
  },

  methods: {
    open() {
      this.dialog = true
    },

    close() {
      this.dialog = false
      this.form = {
        username: '',
        email: '',
        password1: '',
        password2: ''
      }
      if (this.$refs.form) {
        ;(this.$refs.form as any).reset()
      }
    },

    async submit() {
      if (!(this.$refs.form as any).validate()) return

      try {
        await this.$services.auth.register(this.form)
        this.close()
        this.$emit('created')
      } catch (e) {
        console.error(e)
      }
    }
  }
})
</script>