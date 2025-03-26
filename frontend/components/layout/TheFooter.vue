<template>
  <v-footer color="black" class="white--text text-center pa-4">
    <v-container>
      <v-row justify="space-between" align="center">
        <v-col cols="6" class="text-left"> &copy; 2025 Doccana, Software Engineering Lab </v-col>

        <v-col cols="6" class="text-right d-flex align-center justify-end" style="gap: 16px">
          <span>Universidade do Algarve</span>
          <v-btn
            outlined
            style="color: white; margin-left: 0.5vw; border-color: white"
            @click="$router.push(localePath('/about'))"
          >
            About Us
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {}
</script>
