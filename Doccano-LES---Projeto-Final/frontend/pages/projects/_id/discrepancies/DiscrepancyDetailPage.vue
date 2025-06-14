<template>
    <div class="discrepancy-detail-page p-4">
      <h1>Detalhes da Discrepância</h1>
      <!-- Por enquanto está em branco, adicione conteúdo quando quiser -->
    </div>
  </template>
  
  <script>
  export default {
    name: "DiscrepancyDetailPage",
    props: {
      exampleId: {
        type: [String, Number],
        required: false,
      },
    },
    mounted() {
      // caso queira buscar dados via API:
      // this.fetchDiscrepancy(this.exampleId)
    },
    methods: {
      // async fetchDiscrepancy(id) { ... }
    },
  };
  </script>
  
  <style scoped>
  .discrepancy-detail-page {
    /* styles iniciais */
  }
  </style>
  