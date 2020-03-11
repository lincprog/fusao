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
      <Panel title="Resultado da Pesquisa de Empresa" color="secondary" :dark="true" :dense="true">
        <v-sheet
          class="mx-auto"
          elevation="8"
          max-width="800"
        >
          <v-slide-group
            v-model="model"
            class="pa-4"
            multiple
            show-arrows
          >
            <v-slide-item
              v-for="(r, index) in resultado"
              :key="index"
              :value="r"
              v-slot:default="{ active, toggle }"
            >
              <v-card
                :color="active ? 'primary' : 'secondary'"
                class="mx-3"
                max-width="270"
                dark
                elevation="10"
                @click="toggle"
              >
                <v-img
                  v-if="r.logo"
                  height="150px"
                  :src="r.logo"
                >
                </v-img>
                <v-img
                  v-else
                  height="150px"
                  src="../assets/consumidor-logo.png"
                ></v-img>
                <v-card-title v-if="r.companyName">{{ r.companyName }}</v-card-title>
                <v-card-title v-else>{{ r.title }}</v-card-title>
                <v-card-text>
                  {{ r.plataforma }}
                </v-card-text>
                <v-card-actions>
                  <v-btn
                    color="orange"
                    text
                    :target="r.url"
                    :href="r.url"
                  >
                    acessar url
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-chip color="info">
                    {{ r.plataforma }}
                  </v-chip>
                </v-card-actions>
              </v-card>
            </v-slide-item>
          </v-slide-group>
        </v-sheet>
      <template v-slot:acao >
        <v-btn color="info" depressed @click="buscar">fusão e analise</v-btn>
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
        name: 'Americanas',
        platforms: []
      },
      plataformas: [
        { nome: 'Consumidor.gov.br', valor: 'consumidor' },
        { nome: 'Reclameaqui.com.br', valor: 'reclameaqui' }
      ],
      resultado: null,
      model: []
    }
  },
  methods: {
    buscar () {
      axios.get('./data.json')
        .then(response => response.data)
        .then(data => {
          let flat = []
          Object.keys(data).forEach(k => {
            const result = data[k].map(r => {
              return { ...r, plataforma: k }
            })
            flat = [...flat, ...result]
          })
          this.resultado = flat
          console.log(this.resultado)
        }).catch(e => console.log('ERRO:', e))
    }
  }
}
</script>

<style>
</style>
