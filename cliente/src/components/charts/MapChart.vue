<template>
  <chart :constructor-type="'mapChart'" :options="mapOptions" class="map"/>
</template>

<script>
import { Chart } from 'highcharts-vue'
import Highcharts from 'highcharts'
import mapData from '@highcharts/map-collection/countries/br/br-all.geo.json'
import mapInit from 'highcharts/modules/map'

mapInit(Highcharts)
Highcharts.maps.myMapName = mapData

export default {
  components: {
    Chart
  },
  props: ['color', 'titulo', 'dados'],
  data () {
    return {
      mapOptions: {
        chart: {
          map: 'myMapName',
          borderWidth: 1,
          marginRight: 20 // for the legend
        },
        title: {
          text: this.titulo || 'Mapa de Calor do Brasil'
        },
        subtitle: {
          text: 'Origem map: <a href="http://code.highcharts.com/mapdata/countries/br/br-all.js">Brasil</a>'
        },
        mapNavigation: {
          enabled: true,
          buttonOptions: {
            alignTo: 'spacingBox'
          }
        },
        colorAxis: {
          min: 100
        },
        series: [{
          name: 'Quantidade de Reclamações',
          states: {
            hover: {
              color: this.color || '#BADA55'
            }
          },
          dataLabels: {
            enabled: true,
            format: '{point.name}'
          },
          allAreas: true,
          data: this.dados || []
        }]
      }
    }
  }
}
</script>
