<template>
  <Panel title="Pesquisa de Empresas" color="cyan darken-1" :dark="true" :dense="true">
    <v-text-field label="Nome da Empresa" v-model="empresa"></v-text-field>
    <v-select
          v-model="selecao"
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
      <v-btn color="success" depressed @click="buscar">buscar informações</v-btn>
    </template>
  </Panel>
</template>

<script>
import axios from 'axios'
import Panel from '../components/Panel'
export default {
  name: 'Empresa',
  components: { Panel },
  data () {
    return {
      empresa: '',
      selecao: [],
      plataformas: [
        { nome: 'Consumidor.gov.br', valor: 'consumidor' },
        { nome: 'Reclameaqui.com.br', valor: 'reclameaqui' }
      ]
    }
  },
  methods: {
    buscar () {
      axios.get('./data.json')
        .then(response => response.data)
        .then(data => console.log(data))
        .catch(e => console.log('ERRO:', e))
    }
  }
}
</script>

<style>
</style>
