<template>
  <v-row
    class="fill-height"
    justify="center"
    align="center"
  >
    <div class="d-flex flex-column">
      <template v-for="(item, i) in menu">
        <v-hover
          v-slot:default="{ hover }"
          :key="i"
        >
          <v-card
            @click="$router.push(item.rota)"
            class="ma-3"
            max-width="500"
            :elevation="hover ? 12 : 0"
            :class="{ 'on-hover': hover }"
            outlined
          >
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title class="headline mb-1">{{ item.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.subtitle }}</v-list-item-subtitle>
              </v-list-item-content>
              <!-- <v-list-item-avatar
                tile
                size="80"
                color="cyan"
              /> -->
            </v-list-item>
          </v-card>
        </v-hover>
      </template>
    </div>
  </v-row>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      menu: [
        { title: 'Empresa', subtitle: 'Buscar resoluções de uma empresa', rota: '/empresa' },
        { title: 'Dashboard', subtitle: 'Mostrar Análises de suas pesquisas', rota: '/fusao' },
        { title: 'Export', subtitle: 'Exportar suas análises em um arquivo', rota: '/export' }
      ]
    }
  }
}
</script>
