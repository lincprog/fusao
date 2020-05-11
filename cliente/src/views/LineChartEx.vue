<script>
// Importing Line class from the vue-chartjs wrapper
import { Line } from 'vue-chartjs'

// Exporting this so it can be used in other components
export default {
  extends: Line,
  data () {
    return {
      datacollection: {
        // Data to be represented on x-axis
        labels: ['Abril/19', 'Maio/19', 'Junho/19', 'Julho/19', 'Agost/19', 'Setembro/19', 'Outubro/19', 'Novembro/19', 'Dezembro/19', 'Janeiro/20', 'Fevereiro/20', 'Março/20'],
        datasets: [
          {
            label: 'Consumidor.gov.br',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            // Data to be represented on y-axis
            data: [40, 20, 30, 50, 90, 10, 20, 40, 50, 70, 90, 100]
          },
          {
            label: 'reclameaqui',
            borderWidth: 3,
            pointBorderColor: '#f87979',
            // Data to be represented on y-axis
            data: [50, 80, 12, 21, 90, 14, 115, 54, 53, 70, 75, 87]
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
