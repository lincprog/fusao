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
              <v-card-subtitle>Quantidade de reclamações por plataforma </v-card-subtitle>
              <LineChart :chartData="linedata" :options="options" />
              </v-card>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="3">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Reclame Aqui </v-card-subtitle>
              <DoughnutChart :chartData="bardata" :options="options"/>
              </v-card>
            </v-col>
            <v-col cols="3">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Consumidor </v-card-subtitle>
              <PieChart :chartData="piedata" :options="options" />
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
// import BubbleChart from '../components/charts/BubbleChart'
import DoughnutChart from '../components/charts/DoughnutChart'
// import HorizontalBarChart from '../components/charts/HorizontalBarChart'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'
// import PolarAreaChart from '../components/charts/PolarAreaChart'
// import RadarChart from '../components/charts/RadarChart'
// import ScatterChart from '../components/charts/ScatterChart'
import MapChart from '../components/charts/MapChart'

const meses = ['Maio/19', 'Junho/19', 'Julho/19', 'Agost/19', 'Setembro/19', 'Outubro/19', 'Novembro/19', 'Dezembro/19', 'Janeiro/20', 'Fevereiro/20', 'Março/20', 'Abril/20']
const getRandomArbitrary = (max = 500, min = 50) => {
  return Math.floor(Math.random() * (max - min)) + min
}

const getColor = () => {
  const r = getRandomArbitrary(255, 0)
  const g = getRandomArbitrary(255, 0)
  const b = getRandomArbitrary(255, 0)
  return {
    backgroundColor: `rgba(${r},${g},${b},0.2)`,
    borderColor: `rgba(${r},${g},${b},1)`
  }
}

export default {
  name: 'Fusao',
  components: {
    Panel,
    BarChart,
    DoughnutChart,
    LineChart,
    PieChart,
    MapChart
  },
  data () {
    return {
      cores: {
        consumidor: '#41B883',
        reclameaqui: '#E46651'
      },
      doughnutdata: {
        labels: ['Resolvido', 'Nao Resolvido'],
        datasets: [
          {
            data: [67, 33],
            backgroundColor: ['#41B883', '#E46651']
          }
        ]

      },
      piedata: {
        labels: ['Resolvido', 'Nao Resolvido'],
        datasets: [
          {
            data: [59, 61],
            backgroundColor: ['#00D8FF', '#DD1B16']
          }
        ]
      },
      bubbledata: {
        display: true,
        labels: ['Reclame Aqui', 'Consumidor.gov'],
        datasets: [
          {
            label: ['Acre'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Amapá'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 10
            }]
          }, {
            label: ['Roraima'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Pará'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Amazonas'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Maranhão'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Ceará'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Piauí'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rio Grande do Norte'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Pernambuco'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Alagoas'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Paraíba'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Sergipe'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Bahia'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Tocantins'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Goiás'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Mato Grosso'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Mato Grosso do Sul'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rondônia'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Distrito Federal'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Minas Gerais'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['São Paulo'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Espirito Santo'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rio de Janeiro'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Paraná'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Santa Catarina'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rio Grande do Sul'],
            ...getColor(),
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
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
      horizontaldata: {
        labels: [...meses],
        datasets: [
          {
            label: 'Reclame Aqui',
            backgroundColor: '#41B883',
            data: [12, 16, 55, 22, 23, 87, 34, 12, 98, 43, 15, 63]
          },
          {
            label: 'Consumidor.gov',
            backgroundColor: '#E46651',
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
      mapChart: [],
      mapaReclame: [
        ['br-sp', getRandomArbitrary()],
        ['br-ma', getRandomArbitrary()],
        ['br-pa', getRandomArbitrary()],
        ['br-sc', getRandomArbitrary()],
        ['br-ba', getRandomArbitrary()],
        ['br-ap', getRandomArbitrary()],
        ['br-ms', getRandomArbitrary()],
        ['br-mg', getRandomArbitrary()],
        ['br-go', getRandomArbitrary()],
        ['br-rs', getRandomArbitrary()],
        ['br-to', getRandomArbitrary()],
        ['br-pi', getRandomArbitrary()],
        ['br-al', getRandomArbitrary()],
        ['br-pb', getRandomArbitrary()],
        ['br-ce', getRandomArbitrary()],
        ['br-se', getRandomArbitrary()],
        ['br-rr', getRandomArbitrary()],
        ['br-pe', getRandomArbitrary()],
        ['br-pr', getRandomArbitrary()],
        ['br-es', getRandomArbitrary()],
        ['br-rj', getRandomArbitrary()],
        ['br-rn', getRandomArbitrary()],
        ['br-am', getRandomArbitrary()],
        ['br-mt', getRandomArbitrary()],
        ['br-df', getRandomArbitrary()],
        ['br-ac', getRandomArbitrary()],
        ['br-ro', getRandomArbitrary()]
      ]
    }
  },
  created () {
    this.buscar()
  },
  methods: {
    buscar () {
      axios.get('./analysis.json')
        .then(response => response.data)
        .then(data => {
          console.log(data)
          const amounts = data.amounts
          const countStates = data.count_states
          const countDates = data.count_dates
          // , count_dates, count_states, sentiments, topics
          this.montaBarData(amounts)
          this.montaMapChart(countStates)
          this.montaLineData(countDates)
        }).catch(e => console.log('ERRO:', e))
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
      const datas2018 = ['4/2018', '5/2018', '6/2018', '7/2018', '8/2018', '9/2018', '10/2018', '11/2018', '12/2018']
      const datas2019 = ['1/2019', '2/2019', '3/2019', '4/2019', '5/2019', '6/2019', '7/2019', '8/2019', '9/2019', '10/2019', '11/2019', '12/2019']
      const datas2020 = ['1/2020', '2/2020', '3/2020', '4/2020', '5/2020', '6/2020', '7/2020']
      const meses = new Set([...datas2018, ...datas2019, ...datas2020])
      // console.log('meses antes', meses)
      // for (const plataforma in countDates) {
      //   for (const data in countDates[plataforma]) {
      //     meses.add(data)
      //   }
      // }
      // console.log('meses depois', meses)
      const lineData = { ...this.linedata }
      lineData.labels = [...meses]
      for (const plataforma in countDates) {
        const amostragem = []
        for (const data of meses) {
          if (data in countDates[plataforma]) {
            amostragem.push(countDates[plataforma][data])
          } else {
            amostragem.push(0)
          }
        }
        const dataSet = { label: plataforma, data: [...amostragem], backgroundColor: this.cores[plataforma] }
        lineData.datasets.push(dataSet)
      }
      console.log('lineData', lineData)
      this.linedata = { ...lineData }
    }
  }
}
</script>
linedata: {
        labels: [...meses],
        datasets: [
          {
            label: 'Reclame Aqui',
            backgroundColor: '#41B883',
            data: [12, 16, 55, 22, 23, 87, 34, 12, 98, 43, 15, 63]
          },
          {
            label: 'Consumidor.gov',
            backgroundColor: '#E46651',
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
          }
        ]
      }
