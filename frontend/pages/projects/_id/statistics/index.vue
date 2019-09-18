<template>
  <v-container fluid>
    <v-row>
      <v-col
        cols="12"
        lg="4"
      >
        <v-card>
          <doughnut-chart
            :chart-data="progressStat"
          />
        </v-card>
      </v-col>
      <v-col
        cols="12"
        lg="4"
      >
        <v-card>
          <bar-chart
            :chart-data="labelStat"
          />
        </v-card>
      </v-col>
      <v-col
        cols="12"
        lg="4"
      >
        <v-card>
          <bar-chart
            :chart-data="userStat"
          />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DoughnutChart from '@/components/molecules/DoughnutChart'
import BarChart from '@/components/molecules/BarChart'
import StatisticsService from '@/services/statistics.service'

export default {
  layout: 'project',

  components: {
    DoughnutChart,
    BarChart
  },

  data() {
    return {
      progressStat: {},
      userStat: {},
      labelStat: {}
    }
  },

  created() {
    StatisticsService.getStatistics().then((response) => {
      this.labelStat = this.makeData(response.label, 'Label stats')
      this.userStat = this.makeData(response.user, 'User stats')
      const complete = response.total - response.remaining
      const incomplete = response.remaining
      this.progressStat = {
        datasets: [{
          data: [complete, incomplete],
          backgroundColor: ['#00d1b2', '#ffdd57']
        }],

        labels: [
          'Completed',
          'Incomplete'
        ]
      }
    })
  },

  methods: {
    makeData(object, label) {
      const labels = Object.keys(object)
      const counts = Object.values(object)
      const res = {
        labels: labels,
        datasets: [{
          label: label,
          backgroundColor: '#00d1b2',
          data: counts
        }]
      }
      return res
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
