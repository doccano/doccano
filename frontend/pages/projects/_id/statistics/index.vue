<template>
  <v-row v-if="!isEmpty">
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <v-card-title>{{ $t('members.roles.annotator') }}</v-card-title>
        <v-card-text>
          <doughnut-chart
            :chart-data="stats.annotatorProgress"
          />
        </v-card-text>
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <v-card-title>{{ $t('members.roles.annotationApprover') }}</v-card-title>
        <v-card-text>
          <doughnut-chart
            :chart-data="stats.approverProgress"
          />
        </v-card-text>
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <v-card-title>{{ $t('members.roles.projectAdmin') }}</v-card-title>
        <v-card-text>
          <doughnut-chart
            :chart-data="stats.adminProgress"
          />
        </v-card-text>
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <v-card-title>Label Stats</v-card-title>
        <v-card-text>
          <bar-chart
            :chart-data="stats.label"
          />
        </v-card-text>
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <v-card-title>User Stats</v-card-title>
        <v-card-text>
          <bar-chart
            :chart-data="stats.user"
          />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import _ from 'lodash'
import DoughnutChart from '@/components/statistics/ChartDoughnut'
import BarChart from '@/components/statistics/ChartBar'

export default {

  components: {
    DoughnutChart,
    BarChart
  },
  layout: 'project',

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      stats: {}
    }
  },

  computed: {
    isEmpty() {
      return _.isEmpty(this.stats)
    }
  },

  async created() {
    this.stats = await this.$services.statistics.fetchStatistics(
      this.$route.params.id,
      this.$t('statistics.labelStats'),
      this.$t('statistics.userStats'),
      this.$t('statistics.progress')
    )
  }
}
</script>
