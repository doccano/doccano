<template>
  <v-card>
    <v-card-title v-if="isStaff">
      <v-btn class="text-capitalize" color="primary" @click.stop="dialogCreate = true">
        {{ $t('generic.create') }}
      </v-btn>
      <v-dialog v-model="dialogCreate">
        <form-create @cancel="dialogCreate = false" @save="onSave" />
      </v-dialog>

      <v-btn
        class="text-capitalize ms-2"
        :disabled="!canDelete"
        outlined
        @click.stop="dialogDelete = true"
      >
        {{ $t('generic.delete') }}
      </v-btn>
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-card-title>

    <users-list
        v-model="selected"
        :items="users.items"
        :is-loading="isLoading"
        :total="users.count"
        @update:query="updateQuery"
        @search="onSearch"
    />
  </v-card>
</template>

<script lang="ts">
import _ from 'lodash'
import Vue from 'vue'
import { mapGetters } from 'vuex'
import UsersList from '@/components/users/UsersList.vue'
import FormDelete from '@/components/users/FormDelete.vue'
import FormCreate from '@/components/settings/FormCreate.vue'
import { Page } from '~/domain/models/page'
import { User } from '~/domain/models/user'
import { SearchQueryData } from '~/services/application/user/userApplicationService'

export default Vue.extend({
  components: {
    UsersList,
    FormDelete,
    FormCreate
  },
  layout: 'projects',
  middleware: ['check-auth', 'auth'],

  data() {
    return {
      dialogCreate: false,
      dialogDelete: false,
      users: new Page<User>(0, null, null, []),
      selected: [] as User[],
      isLoading: false
    }
  },

  async fetch() {
    await this.fetchUsers()
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    canDelete(): boolean {
      return this.selected.length > 0
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      this.$fetch()
    }, 500)
  },

  methods: {
    async fetchUsers() {
      this.isLoading = true
      try {
        this.users = await this.$repositories.user.list(this.$route.query as SearchQueryData)
      } catch (error) {
        console.error('Erro ao buscar usuários:', error)
      }
      this.isLoading = false
    },

    updateQuery({ query }: { query: any }) {
  this.$router.push({ query })
  },

    onSearch(search: string) {
      const query = { ...this.$route.query, q: search }
      this.updateQuery(query)
    },

    onSave() {
      this.dialogCreate = false
      this.$fetch()
    },

    async remove() {
      try {
        console.log("Iniciando remoção de usuários. Selecionados:", this.selected);
        const ids = this.selected.map(user => user.id);
        console.log("IDs dos usuários a serem deletados:", ids);
        await this.$repositories.user.bulkDelete(ids);
        console.log("Exclusão em lote realizada com sucesso.");
        await this.$fetch();
        this.dialogDelete = false;
        this.selected = [];
        console.log("Dialog de deleção fechado e seleção limpa.");
      } catch (error) {
        console.error("Erro ao deletar usuários:", error);
      }
}



  }
})
</script>
