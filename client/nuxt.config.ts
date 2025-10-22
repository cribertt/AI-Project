// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
   app: {
    baseURL: '/inacap/',     // 👈 MUY importante el slash inicial y final
    buildAssetsDir: '/_nuxt/' // opcional; con slash inicial (default ya es /_nuxt/)
  },
  devtools: { enabled: true },
  ssr: false, 
})
