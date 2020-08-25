<template>
  <v-row>
    <v-col cols="12" v-show="resultado == null">
      <Panel title="Pesquisa Inicial" color="primary" :dark="true" :dense="true">
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
          <v-btn color="success" depressed @click="buscar">buscar informações</v-btn>
        </template>
      </Panel>
    </v-col>
    <v-col cols="12" v-show="resultado != null">
      <Panel :title="'Resultado encontrados para '+empresa.name" color="info" :dark="true" :dense="true">
        <v-sheet
          class="mx-auto"
          elevation="8"
          max-width="900"
        >
          <v-expansion-panels
            v-model="painel"
            multiple
          >
            <v-expansion-panel v-for="(res, plat , index) in resultado" :key="index">
              <v-expansion-panel-header><h4>{{ `${res.length} itens encontrados para ${plat}` }} </h4>
                </v-expansion-panel-header>
              <v-expansion-panel-content>
                  <v-slide-group
                    v-model="model"
                    class="pa-2"
                    multiple
                    show-arrows
                  >
                    <v-slide-item
                      v-for="(r, index) in res"
                      :key="index"
                      :value="r"
                      v-slot:default="{ active, toggle }"
                    >
                      <v-card
                        :color="active ? 'accent' : 'primary'"
                        class="mx-3"
                        max-width="270"
                        dark
                        elevation="10"
                        @click="toggle"
                      >
                        <v-img
                          v-if="r.logo"
                          height="100px"
                          :src="r.logo"
                        ></v-img>
                        <v-img
                          v-else
                          height="100px"
                          src="../assets/consumidor-logo.png"
                        ></v-img>
                        <v-card-title v-if="r.companyName">{{ r.companyName }}</v-card-title>
                        <v-card-title v-else>{{ r.title }}</v-card-title>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            color="white"
                            text
                            :target="r.url"
                            :href="r.url"
                          >
                            acessar url
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-slide-item>
                  </v-slide-group>
                </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-sheet>
      <template v-slot:acao >
        <v-btn color="success" depressed to="fusao">fusão e analise</v-btn>
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
      model: [],
      painel: []
    }
  },
  methods: {
    buscar () {
      axios.get('./collections/name.json')
        .then(response => response.data)
        .then(data => {
          this.resultado = data
        }).catch(e => console.log('ERRO:', e))
    }
  }
}
</script>

<style>
</style>
