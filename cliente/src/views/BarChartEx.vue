<script>
// Importing Bar class from the vue-chartjs wrapper
import { Bar } from 'vue-chartjs'
// Exporting this so it can be used in other components
export default {
  extends: Bar,
  data () {
    return {
      datacollection: {
        // Data to be represented on x-axis
        labels: ['consumidor.gov.br', 'reclameaqui'],
        datasets: [
          {
            label: 'Quantidade de Reclamaçoes',
            backgroundColor: '#f87979',
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            // Data to be represented on y-axis
            data: [359, 123]
          }
        ]
      },
      // Chart.js options that controls the appearance of the chart
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: true
            }
          }],
          xAxes: [{
            gridLines: {
              display: false
            }
          }]
        },
        legend: {
          display: true
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  mounted () {
    // renderChart function renders the chart with the datacollection and options object.
    this.renderChart(this.datacollection, this.options)
  }
}
</script>
