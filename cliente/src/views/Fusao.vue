<template>
  <v-row>
<!-- // #2 Visualizações das análises (gráficos):

// Quantidade de reclamações por plataforma;
// Distribuição quantitativa pelo período (gráfico linha);
// Percentual resolvido/não resolvido (gráfico pizza);
// Distribuição geográfica (mapa de calor ou de clusters);
// Análise de sentimentos (gráfico pizza);
// Análise de tópicos (não é gráfico). -->
    <v-col cols="12">
      <Panel title="Resultados para empresa Americanas 04/19 ate 04/20" color="primary" :dark="true" :dense="true">
        <v-container class="grey lighten-5">
          <v-row>
            <v-col cols="6">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Quantidade de reclamações por plataforma </v-card-subtitle>
              <BarChart :chartData="bardata" :options="options"/>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Histórico de Reclamações nos últimos meses</v-card-subtitle>
              <LineChart :chartData="linedata" :options="options" />
              </v-card>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Análise de Sentimentos</v-card-subtitle>
              <DoughnutChart :chartData="piedata" :options="options"/>
              </v-card>
            </v-col>
            <v-col cols="6">
              <map-chart v-if="mapChart.length" :dados="mapChart" color="orange" titulo="Mapa de Calor"/>
            </v-col>
          </v-row>
        </v-container>
      </Panel>
    </v-col>
  </v-row>
</template>

<script>

import axios from 'axios'
import Panel from '../components/Panel'
import BarChart from '../components/charts/BarChart'
import DoughnutChart from '../components/charts/DoughnutChart'
import LineChart from '../components/charts/LineChart'
// import PieChart from '../components/charts/PieChart'
import MapChart from '../components/charts/MapChart'

const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

export default {
  name: 'Fusao',
  components: {
    Panel,
    BarChart,
    DoughnutChart,
    LineChart,
    MapChart
  },
  data () {
    return {
      legenda: {
        negative_medium: 'Mais Negativo',
        negative: 'Negativo',
        neutral: 'Neutro',
        positive: 'Positivo',
        positive_medium: 'Mais Positivo'
      },
      cores: {
        consumidor: '#41B883',
        reclameaqui: '#E46651'
      },
      piedata: {
        labels: [],
        datasets: [
          {
            data: [],
            backgroundColor: ['#00D8FF', '#DD1B16', '#41B883', '#E46651', '#E32451']
          }
        ]
      },
      linedata: {
        labels: [],
        datasets: []
      },
      bardata: {
        labels: [],
        datasets: [
          {
            label: 'Quantidade',
            backgroundColor: '#41B883',
            data: []
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
      mapChart: []
    }
  },
  created () {
    this.buscar()
    console.log(meses)
  },
  methods: {
    buscar () {
      axios.get('./collections/nubank_novo.json')
        .then(response => response.data)
        .then(data => {
          console.log(data)
          const amounts = data.amounts
          const countStates = data.count_states
          const countDates = data.count_dates
          const sentiments = data.sentiments
          // , count_dates, count_states, sentiments, topics
          this.montaBarData(amounts)
          this.montaMapChart(countStates)
          this.montaLineData(countDates)
          this.montaPieData(sentiments)
        }).catch(e => console.log('ERRO:', e))
    },
    montaPieData (sentiments) {
      const pieData = { ...this.piedata }
      for (const key in sentiments) {
        const element = sentiments[key]
        pieData.labels.push(this.legenda[key])
        pieData.datasets[0].data.push(element)
        pieData.datasets[0].backgroundColor.push()
      }
      this.piedata = { ...pieData }
    },
    montaBarData (amounts) {
      const barData = { ...this.bardata }
      for (const key in amounts) {
        const element = amounts[key]
        barData.labels.push(key)
        barData.datasets[0].data.push(element)
      }
      this.bardata = { ...barData }
    },
    montaMapChart (countStates) {
      const mapChart = [...this.mapChart]
      for (const key in countStates) {
        const qtd = countStates[key]
        const state = [`br-${key}`.toLowerCase(), qtd]
        mapChart.push(state)
      }
      this.mapChart = [...mapChart]
    },
    montaLineData (countDates) {
      const datas2018 = ['Abril/2018', 'Maio/2018', 'Junho/2018', 'Julho/2018', 'Agosto/2018', 'Setembro/2018', 'Outubro/2018', 'Novembro/2018', 'Dezembro/2018']
      const datas2019 = ['Janeiro/2019', 'Fevereiro/2019', 'Marco/2019', 'Abril/2019', 'Maio/2019', 'Junho/2019', 'Julho/2019', 'Agosto/2019', 'Setembro/2019', 'Outubro/2019', 'Novembro/2019', 'Dezembro/2019']
      const datas2020 = ['Janeiro/2020', 'Fevereiro/2020', 'Marco/2020', 'Abril/2020', 'Maio/2020', 'Junho/2020', 'Julho/2020', 'Agosto/2020']
      const meses = new Set([...datas2018, ...datas2019, ...datas2020])
      const labels = new Set()
      const lineData = { ...this.linedata }
      for (const plataforma in countDates) {
        const amostragem = []
        for (const mes of meses) {
          const keys = Object.keys(countDates)
          let hasMes = false
          keys.forEach(k => {
            hasMes = hasMes || mes in countDates[k]
          })
          if (hasMes) {
            labels.add(mes)
            if (mes in countDates[plataforma]) {
              amostragem.push(countDates[plataforma][mes])
            } else {
              amostragem.push(0)
            }
          }
        }
        lineData.labels = [...labels]
        const dataSet = { label: plataforma, data: [...amostragem], backgroundColor: this.cores[plataforma] }
        lineData.datasets.push(dataSet)
      }
      console.log('lineData', lineData)
      this.linedata = { ...lineData }
    }
  }
}
</script>
