export default {
  locales: [
    {
      name: 'English',
      code: 'en',
      iso: 'en-CA',
      file: 'en'
    },
    {
      name: 'Français',
      code: 'fr',
      iso: 'fr-CA',
      file: 'fr'
    }
  ],
  lazy: true,
  langDir: 'i18n/',
  defaultLocale: 'en',
  vueI18n: {
    fallbackLocale: 'en'
  }
}
