<script>
import { HorizontalBar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: HorizontalBar,
  mixins: [reactiveProp],
  props: {
    chartData: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  data() {
    return {
      options: {
        scales: {
          yAxes: [
            {
              barPercentage: 0.3
            }
          ],
          xAxes: [
            {
              ticks: {
                beginAtZero: true,
                min: 0
              }
            }
          ]
        },
        maintainAspectRatio: false,
        legend: {
          display: false
        }
      }
    }
  },

  mounted() {
    this.renderChart(this.chartData, this.options)
  }
}
</script>
