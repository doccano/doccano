<template>
  <v-footer color="black" class="white--text text-center pa-4">
    <v-container>
      <v-row justify="space-between" align="center">
        <!-- Texto do copyright à esquerda -->
        <v-col cols="6" class="text-left">
          &copy; {{ new Date().getFullYear() }} Doccano
        </v-col>

        <!-- Universidade do Algarve à direita -->
        <v-col cols="6" class="text-right">
          Universidade do Algarve
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {
}
</script>
