import {
    HorizontalBar,
    mixins
} from 'vue-chartjs'
const {
    reactiveProp,
    reactiveData
} = mixins

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
var base_url = window.location.href.split('/').slice(3, 5).join('/');
const HTTP = axios.create({
    baseURL: `/api/${base_url}/`,
})


Vue.component('line-chart', {
    extends: HorizontalBar,
    mixins: [reactiveProp],
    props: ['chartData'],
    data: function () {
        return {
            options: {
                scales: {
                    yAxes: [{
                        barPercentage: 0.3,
                    }],
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,
                            min: 0
                        }
                    }]
                },
                maintainAspectRatio: false,
            }
        }
    },
    mounted() {
        this.renderChart(this.chartData, this.options)
    }
})

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    data: {
        labelData: null,
        userData: null
    },

    methods: {
        makeData(data, labels, label) {
            var data = {
                labels: labels,
                datasets: [{
                    label: label,
                    backgroundColor: '#00d1b2',
                    data: data
                }]
            }
            return data
        }
    },

    created: function () {
        HTTP.get('stats').then(response => {
            this.labelData = this.makeData(response.data.label.data, response.data.label.labels, 'Label stats');
            this.userData = this.makeData(response.data.user.data, response.data.user.users, 'User stats');
        })
    }
})