<template>
  <v-row>
    <v-col cols="12" v-show="resultado == null">
      <Panel title="Pesquisa de Empresas" color="cyan darken-1" :dark="true" :dense="true">
        <v-text-field label="Nome da Empresa" v-model="empresa.name"></v-text-field>
        <v-select
              v-model="empresa.platforms"
              :items="plataformas"
              label="Plataformas"
              item-text="nome"
              item-value="valor"
              multiple
              chips
              hint="sites para pesquisa"
              persistent-hint
            ></v-select>
        <template v-slot:acao >
          <v-btn color="info" depressed @click="buscar">buscar informações</v-btn>
        </template>
      </Panel>
    </v-col>
    <v-col cols="12" v-show="resultado != null">
      <Panel title="Resultado da Pesquisa" color="secondary" :dark="true" :dense="true">
      <template v-slot:acao >
        <v-btn color="info" depressed @click="buscar">buscar informações</v-btn>
        </template>
      </Panel>
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios'
import Panel from '../components/Panel'
export default {
  name: 'Empresa',
  components: { Panel },
  data () {
    return {
      empresa: {
        name: null,
        platforms: []
      },
      plataformas: [
        { nome: 'Consumidor.gov.br', valor: 'consumidor' },
        { nome: 'Reclameaqui.com.br', valor: 'reclameaqui' }
      ],
      resultado: null
    }
  },
  methods: {
    buscar () {
      axios.get('./data.json')
        .then(response => response.data)
        .then(data => {
          this.resultado = data
          console.log(this.resultado)
        }).catch(e => console.log('ERRO:', e))
    }
  }
}
</script>

<style>
</style>
