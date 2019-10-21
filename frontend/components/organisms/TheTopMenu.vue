<template>
  <v-menu bottom left>
    <template v-slot:activator="{ on }">
      <v-btn
        icon
        v-on="on"
      >
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </template>

    <v-list>
      <v-list-item>
        <v-list-item-icon>
          <v-icon>mdi-settings</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            Dark Theme
          </v-list-item-title>
        </v-list-item-content>
        <v-list-item-action>
          <v-switch v-model="isDark" />
        </v-list-item-action>
      </v-list-item>
      <v-list-item>
        <v-list-item-icon>
          <v-icon>mdi-translate</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            RTL
          </v-list-item-title>
        </v-list-item-content>
        <v-list-item-action>
          <v-switch v-model="isRTL" />
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  data() {
    return {
      isDark: false,
      isRTL: false
    }
  },

  watch: {
    isDark() {
      this.$vuetify.theme.themes = {
        dark: {
          primary: '#21CFF3',
          accent: '#FF4081',
          secondary: '#ffe18d',
          success: '#4CAF50',
          info: '#2196F3',
          warning: '#FB8C00',
          error: '#FF5252'
        },
        light: {
          primary: '#1976D2',
          accent: '#e91e63',
          secondary: '#30b1dc',
          success: '#4CAF50',
          info: '#2196F3',
          warning: '#FB8C00',
          error: '#FF5252'
        }
      }
      this.$vuetify.theme.dark = this.isDark
      localStorage.setItem('dark', this.isDark)
    },
    isRTL() {
      this.$vuetify.rtl = this.isRTL
      localStorage.setItem('rtl', this.isRTL)
    }
  },

  created() {
    const dark = localStorage.getItem('dark')
    const rtl = localStorage.getItem('rtl')
    this.isDark = dark ? JSON.parse(dark) : false
    this.isRTL = rtl ? JSON.parse(rtl) : false
  }
}
</script>
