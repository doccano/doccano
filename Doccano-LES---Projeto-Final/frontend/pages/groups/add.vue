<template>
  <v-container class="pt-5">
    <v-card>
      <v-card-title>Add group</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field v-model="groupName" label="Name" outlined dense></v-text-field>
          <v-autocomplete
            v-model="selectedPermissions"
            :items="permissions"
            label="Permissions"
            multiple
            chips
            small-chips
            outlined
            dense
            attach
            return-object
            item-text="name"
            item-value="id"
          ></v-autocomplete>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="saveGroup">Save</v-btn>
        <v-btn color="primary" outlined @click="saveAndAddAnother">Save and add another</v-btn>
        <v-btn color="primary" outlined @click="saveAndContinueEditing"
          >Save and continue editing</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios' // Importa o Axios para fazer chamadas HTTP

export default {
  layout: 'projects',

  data() {
    return {
      groupName: '',
      selectedPermissions: [],
      permissions: [] // Inicialmente vazio, será preenchido com dados da API
    }
  },
  mounted() {
    this.fetchPermissions() // Busca as permissões quando o componente é carregado
  },
  methods: {
    fetchPermissions() {
      axios
        .get('http://127.0.0.1:8000/api/permissions') // Ajuste a URL conforme necessário
        .then((response) => {
          this.permissions = response.data // Armazena as permissões no data model
        })
        .catch((error) => {
          console.error('Error fetching permissions:', error)
        })
    },
    saveGroup() {
      // Implemente a lógica de salvar o grupo aqui
      console.log('Saving group with name:', this.groupName)
      console.log('Selected permissions:', this.selectedPermissions)
    },
    saveAndAddAnother() {
      this.saveGroup()
      this.resetForm()
    },
    saveAndContinueEditing() {
      this.saveGroup()
    },
    resetForm() {
      this.groupName = ''
      this.selectedPermissions = []
    }
  }
}
</script>

<style scoped>
.v-container {
  padding-top: 100px; /* Espaço suficiente para evitar sobreposição com o menu */
}
</style>
