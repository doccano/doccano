<template>
    <div class="p-6">
      <h1>Discrepância — Exemplo {{ exampleId }}</h1>
      <!-- Conteúdo a adicionar depois -->
    </div>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  
  export default Vue.extend({
    name: 'DiscrepancyDetailPage',
    props: {
      exampleId: {
        type: [String, Number],
        required: true,
      },
    },
  })
  </script>
  
  <style scoped>
  /* estilos iniciais */
  </style>
  