<template>
  <v-row v-if="stats">
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <doughnut-chart
          :chart-data="progressLocale()"
        />
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <bar-chart
          :chart-data="labelStatsLocale()"
        />
      </v-card>
    </v-col>
    <v-col
      cols="12"
      lg="4"
    >
      <v-card>
        <bar-chart
          :chart-data="userStatsLocale()"
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import DoughnutChart from '@/components/molecules/DoughnutChart'
import BarChart from '@/components/molecules/BarChart'

export default {
  layout: 'project',

  components: {
    DoughnutChart,
    BarChart
  },

  computed: {
    ...mapGetters('statistics', ['userStats', 'labelStats', 'progress']),
    ...mapState('statistics', ['stats'])
  },

  async created() {
    await this.fetchStatistics({
      projectId: this.$route.params.id
    })
  },

  methods: {
    ...mapActions('statistics', ['fetchStatistics']),
    progressLocale() {
      return this.progress(this.$t('statistics.progress'))
    },
    labelStatsLocale() {
      return this.labelStats(this.$t('statistics.labelStats'))
    },
    userStatsLocale() {
      return this.userStats(this.$t('statistics.userStats'))
    }
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
