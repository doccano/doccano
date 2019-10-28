<template>
  <v-container
    v-if="stats"
    fluid
  >
    <v-row>
      <v-col
        cols="12"
        lg="4"
      >
        <v-card>
          <doughnut-chart
            :chart-data="progress"
          />
        </v-card>
      </v-col>
      <v-col
        cols="12"
        lg="4"
      >
        <v-card>
          <bar-chart
            :chart-data="labelStats"
          />
        </v-card>
      </v-col>
      <v-col
        cols="12"
        lg="4"
      >
        <v-card>
          <bar-chart
            :chart-data="userStats"
          />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import DoughnutChart from '@/components/molecules/DoughnutChart'
import BarChart from '@/components/molecules/BarChart'

export default {
  layout: 'project',

  middleware: 'check-auth',

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
    ...mapActions('statistics', ['fetchStatistics'])
  },

  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
