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
            <v-col cols="3">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Quantidade de reclamações por plataforma </v-card-subtitle>
              <BarChart :chartData="bardata" :options="options"/>
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Reclamações por plataforma durante o periodo </v-card-subtitle>
              <HorizontalBarChart :chartData="horizontaldata" :options="options"/>
              </v-card>
            </v-col>
            <v-col cols="5">
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
            <v-col cols="12">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Mapa de Calor</v-card-subtitle>
              <BubbleChart :chartData="bubbledata" :options="options" />
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Reclame Aqui </v-card-subtitle>
              <DoughnutChart :chartData="doughnutdata" :options="options"/>
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Consumidor </v-card-subtitle>
              <PieChart :chartData="piedata" :options="options" />
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Quantidade de reclamações por plataforma </v-card-subtitle>
              <PolarAreaChart :chartData="polardata" :options="options" />
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Quantidade de reclamações por plataforma </v-card-subtitle>
              <RadarChart :chartData="radardata" :options="options" />
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card
                class="pa-2"
                outlined
                tile
              >
              <v-card-subtitle>Quantidade de reclamações por plataforma </v-card-subtitle>
              <ScatterChart :chartData="scatterdata" :options="options" />
              </v-card>
            </v-col>
            <v-col cols="6">
              <map-chart :dados="mapaReclame" color="orange" titulo="Reclame Aqui"/>
            </v-col>
            <v-col cols="6">
              <map-chart :dados="mapaConsumidor" color="cyan" titulo="Consumidor"/>
            </v-col>
          </v-row>
        </v-container>
      </Panel>
    </v-col>
  </v-row>
</template>

<script>
import Panel from '../components/Panel'
import BarChart from '../components/charts/BarChart'
import BubbleChart from '../components/charts/BubbleChart'
import DoughnutChart from '../components/charts/DoughnutChart'
import HorizontalBarChart from '../components/charts/HorizontalBarChart'
import LineChart from '../components/charts/LineChart'
import PieChart from '../components/charts/PieChart'
import PolarAreaChart from '../components/charts/PolarAreaChart'
import RadarChart from '../components/charts/RadarChart'
import ScatterChart from '../components/charts/ScatterChart'
import MapChart from '../components/charts/MapChart'

const meses = ['Maio/19', 'Junho/19', 'Julho/19', 'Agost/19', 'Setembro/19', 'Outubro/19', 'Novembro/19', 'Dezembro/19', 'Janeiro/20', 'Fevereiro/20', 'Março/20', 'Abril/20']
const getRandomArbitrary = () => {
  const max = 500
  const min = 50
  return Math.floor(Math.random() * (max - min)) + min
}

export default {
  name: 'Fusao',
  components: {
    Panel,
    BarChart,
    BubbleChart,
    DoughnutChart,
    HorizontalBarChart,
    LineChart,
    PieChart,
    PolarAreaChart,
    RadarChart,
    ScatterChart,
    MapChart
  },
  data () {
    return {
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
        datasets: [
          {
            label: ['Acre'],
            backgroundColor: 'rgba(255,221,50,0.2)',
            borderColor: 'rgba(255,221,50,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Amapá'],
            backgroundColor: 'rgba(60,186,159,0.2)',
            borderColor: 'rgba(60,186,159,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 10
            }]
          }, {
            label: ['Roraima'],
            backgroundColor: 'rgba(0,0,0,0.2)',
            borderColor: '#000',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Pará'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Amazonas'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Maranhão'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Ceará'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Piauí'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rio Grande do Norte'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Pernambuco'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Alagoas'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Paraíba'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Sergipe'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Bahia'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Tocantins'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Goiás'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Mato Grosso'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Mato Grosso do Sul'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rondônia'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Distrito Federal'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Minas Gerais'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['São Paulo'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Espirito Santo'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rio de Janeiro'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Paraná'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Santa Catarina'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }, {
            label: ['Rio Grande do Sul'],
            backgroundColor: 'rgba(193,46,12,0.2)',
            borderColor: 'rgba(193,46,12,1)',
            data: [{
              x: getRandomArbitrary(),
              y: getRandomArbitrary(),
              r: 15
            }]
          }
        ]
      },
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
      },
      bardata: {
        labels: ['Reclame Aqui', 'Consumidor.gov'],
        datasets: [
          {
            label: 'Quantidade',
            backgroundColor: '#f87979',
            data: [1326, 1178]
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
      polardata: {
        labels: ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'],
        datasets: [
          {
            label: 'My First dataset',
            backgroundColor: 'rgba(179,181,198,0.2)',
            pointBackgroundColor: 'rgba(179,181,198,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(179,181,198,1)',
            data: [65, 59, 90, 81, 56, 55, 40]
          },
          {
            label: 'My Second dataset',
            backgroundColor: 'rgba(255,99,132,0.2)',
            pointBackgroundColor: 'rgba(255,99,132,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(255,99,132,1)',
            data: [28, 48, 40, 19, 96, 27, 100]
          }
        ]
      },
      radardata: {
        labels: ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'],
        datasets: [
          {
            label: 'My First dataset',
            backgroundColor: 'rgba(179,181,198,0.2)',
            borderColor: 'rgba(179,181,198,1)',
            pointBackgroundColor: 'rgba(179,181,198,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(179,181,198,1)',
            data: [65, 59, 90, 81, 56, 55, 40]
          },
          {
            label: 'My Second dataset',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            pointBackgroundColor: 'rgba(255,99,132,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(255,99,132,1)',
            data: [28, 48, 40, 19, 96, 27, 100]
          }
        ]
      },
      scatterdata: {
        datasets: [{
          label: 'Reclame Aqui',
          fill: false,
          borderColor: '#f87979',
          backgroundColor: '#f87979',
          data: [{
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }]
        },
        {
          label: 'Consumidor.gov.br',
          fill: false,
          borderColor: '#7acbf9',
          backgroundColor: '#7acbf9',
          data: [{
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }, {
            x: getRandomArbitrary(),
            y: getRandomArbitrary()
          }]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
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
      ],
      mapaConsumidor: [
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
        ['br-ro', getRandomArbitrary()]]
    }
  },
  mounted () {
  },
  methods: {
  }
}
</script>

<style>

</style>
