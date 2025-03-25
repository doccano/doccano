<!-- eslint-disable max-len -->

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
      // Inicializa o objeto Page com propriedades padrão (contando com "items" e "count")
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
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  methods: {
    async fetchUsers() {
      this.isLoading = true
      try {

        // eslint-disable-next-line max-len
        this.users = await this.$repositories.user.list(this.$route.query as unknown as SearchQueryData)
      } catch (error) {
        console.error('Erro ao buscar usuários:', error)
      }
      this.isLoading = false
    },
    updateQuery(query: object) {
      this.$router.push({ query })
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

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>
