<template>
  <v-footer color="black" class="white--text text-center pa-6">
    <v-container>
      <v-row justify="center">
        <!-- Logo -->
        <v-col cols="12">
          <v-img src="/logo.png" contain height="50" class="mx-auto"></v-img>
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-3">
        <v-col cols="12">
          <p class="mb-0">&copy; {{ new Date().getFullYear() }} Doccano. All rights reserved.</p>
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-4">
        <!-- Ícones de redes sociais -->
        <v-col cols="12" class="d-flex justify-center">
          <v-btn icon class="social-icon mx-2" href="https://facebook.com" target="_blank">
            <v-icon size="24" class="icon-style">mdi-facebook</v-icon>
          </v-btn>
          <v-btn icon class="social-icon mx-2" href="https://twitter.com" target="_blank">
            <v-icon size="24" class="icon-style">mdi-twitter</v-icon>
          </v-btn>
          <v-btn icon class="social-icon mx-2" href="https://instagram.com" target="_blank">
            <v-icon size="24" class="icon-style">mdi-instagram</v-icon>
          </v-btn>
          <v-btn icon class="social-icon mx-2" href="https://rss.com" target="_blank">
            <v-icon size="24" class="icon-style">mdi-rss</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {
}
</script>

<style scoped>
.v-footer {
  font-size: 14px;
}

/* Ícones com fundo branco e cor preta */
.social-icon {
  background-color: white; /* Fundo branco */
  color: black !important; /* Cor dos ícones */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.social-icon:hover {
  transform: scale(1.1);
  background-color: #ddd;
}

/* Cor preta nos ícones */
.icon-style {
  color: black !important;
}
</style>
