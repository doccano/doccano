import Vue from 'vue';
Vue.use(require('vue-shortkey'), { prevent: ['input', 'textarea'] });
import annotationMixin from './mixin.js';
import HTTP from './http.js';

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    mixins: [annotationMixin],

    methods: {
        addLabel: async function (label_id) {
            for (var i = 0; i < this.items[this.cur]['labels'].length; i++) {
                var item = this.items[this.cur]['labels'][i];
                if (label_id == item.label.id) {
                    this.deleteLabel(i);
                    return;
                }
            }

            var payload = {
                'label_id': label_id
            };

            var doc_id = this.items[this.cur].id;
            await HTTP.post(`docs/${doc_id}/annotations/`, payload).then(response => {
                this.items[this.cur]['labels'].push(response.data);
            })
        }
    }
});