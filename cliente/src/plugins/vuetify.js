import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  icons: {
    iconfont: 'mdi' // 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
  },
  theme: {
    themes: {
      light: {
        primary: '#00bcd4',
        secondary: '#607d8b',
        accent: '#ff9800',
        error: '#f44336',
        warning: '#795548',
        info: '#009688',
        success: '#e91e63'
      }
    }
  }
})
