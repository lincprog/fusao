<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
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
            <v-icon>mdi-settings</v-icon>
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
      dense    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>{{ title + mode }}</v-toolbar-title>
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
          <router-view/>
        </v-row>
      </v-container>
    </v-content>
    <v-footer app>
      <span>&copy; 2019 - EngComp Uema</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  components: {},
  computed: {
  },
  data () {
    return {
      drawer: null,
      title: process.env.VUE_APP_TITLE,
      mode: process.env.VUE_APP_MODE || ''
    }
  },
  methods: {
  }
}
</script>
