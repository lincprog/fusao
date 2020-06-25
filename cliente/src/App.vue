<template>
  <v-app id="inspire">
    <Loading />
    <SnackBar />
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
            <v-icon>mdi-cog</v-icon>
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
      dense
    >
      <v-app-bar-nav-icon
        v-show="isLogged"
        @click.stop="drawer = !drawer"
      />
      <v-toolbar-title>{{ title + mode }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        icon
        to="/"
      >
        <v-icon>mdi-home</v-icon>
      </v-btn>
      <v-btn
        icon
        v-show="isLogged"
      >
        <v-icon @click="exit">mdi-exit-to-app</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container
        fluid
        fill-height
      >
        <router-view />
      </v-container>
    </v-content>
    <v-footer
      app
      dark
      color="primary"
    >
      <span>&copy; 2019 - EngComp Uema</span>
    </v-footer>
  </v-app>
</template>

<script>
import Loading from './components/Loading'
import SnackBar from './components/SnackBar'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'App',
  components: { SnackBar, Loading },
  computed: {
    ...mapGetters(['isLogged'])
  },
  created () {
    this.checkUserToken()
      .then(user => {
        this.setSuccess({ message: `Welcome to back ${user.name}!` })
        this.$router.push({ name: 'Home' })
      })
      .catch(e => {
        this.$router.push({ name: 'Auth' })
      })
  },
  data () {
    return {
      drawer: null,
      title: process.env.VUE_APP_TITLE,
      mode: process.env.VUE_APP_MODE || ''
    }
  },
  methods: {
    ...mapActions(['logout', 'checkUserToken', 'setWarning', 'setSuccess']),
    exit () {
      this.logout()
      this.$router.push({ name: 'Auth' })
    }
  }
}
</script>
