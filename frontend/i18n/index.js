export default {
  locales: [
    {
      name: 'English',
      code: 'en',
      iso: 'en-CA',
      file: 'en'
    },
    {
      name: '中文',
      code: 'zh',
      iso: 'zh-CN',
      file: 'zh'
    },
    {
      name: 'Français',
      code: 'fr',
      iso: 'fr-CA',
      file: 'fr'
    },
    {
      name: 'Deutsch',
      code: 'de',
      iso: 'de-DE',
      file: 'de'
    },
    {
      name: 'Persian',
      code: 'fa',
      iso: 'fa-FA',
      file: 'fa'
    }
  ],
  lazy: true,
  langDir: 'i18n/',
  defaultLocale: 'en',
  vueI18n: {
    fallbackLocale: 'en'
  },
  detectBrowserLanguage: {
    useCookie: true,
    cookieKey: 'i18n_redirected',
    onlyOnRoot: true // for SEO purposes
  }
}
