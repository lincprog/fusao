<template>
  <v-app id="inspire">
    <Loading/>
    <SnackBar/>
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
      color="primary"
      dark
    >
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Configurações</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      app
      clipped-left
      color="primary"
      dark
      dense>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>{{ title + mode }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon @click="logout">mdi-exit-to-app</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
         <v-col cols="12">
          <router-view/>
         </v-col>
        </v-row>
      </v-container>
    </v-content>
    <v-footer
      app
      dark
      color="primary">
      <span>&copy; 2019 - EngComp Uema</span>
    </v-footer>
  </v-app>
</template>

<script>
import Loading from './components/Loading'
import SnackBar from './components/SnackBar'
import { userKey } from './config'
import { mapState } from 'vuex'
export default {
  name: 'App',
  components: { SnackBar, Loading },
  computed: { ...mapState(['isMenuVisible', 'user']) },
  data () {
    return {
      drawer: null,
      title: process.env.VUE_APP_TITLE,
      mode: process.env.VUE_APP_MODE || '',
      validatingToken: true
    }
  },
  methods: {
    logout () {
      localStorage.removeItem(userKey)
      this.$router.push({ name: 'Auth' })
    }
  }
}
</script>
