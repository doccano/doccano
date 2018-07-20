import Vue from 'vue';
Vue.use(require('vue-shortkey'));
import annotationMixin from './mixin.js';
import HTTP from './http.js';

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    mixins: [annotationMixin],

    methods: {
        addLabel: async function (label_id) {
            var payload = {
                'label_id': label_id
            };

            var doc_id = this.items[this.cur].id;
            await HTTP.post(`docs/${doc_id}/annotations/`, payload).then(response => {
                this.items[this.cur]['labels'].push(response.data);
            });
            this.updateProgress();
        }
    },
    created: function () {
        this.updateProgress();
        this.submit();
    }
});