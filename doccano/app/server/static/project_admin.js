axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
var base_url = window.location.href.split('/').slice(3, 5).join('/');


function swap(values) {
    var ret = {};
    for (var item of values) {
        ret[item['text']] = item['id'];
    }
    return ret;
};


Vue.component('tabs', {
    template: `
        <div>
            <div class="tabs is-boxed is-right" style="margin-bottom:0;">
                <ul>
                    <li v-for="tab in tabs" :class="{ 'is-active': tab.isActive }">
                        <a :href="tab.href" @click="selectTab(tab)">{{ tab.name }}</a>
                    </li>
                </ul>
            </div>

            <div class="tabs-details">
                <slot></slot>
            </div>
        </div>
    `,

    data() {
        return {
            tabs: []
        };
    },

    created() {
        this.tabs = this.$children;
    },

    methods: {
        selectTab(selectedTab) {
            this.tabs.forEach(tab => {
                tab.isActive = (tab.name == selectedTab.name);
            });
        }
    }

});

Vue.component('tab', {
    template: `
        <div v-show="isActive"><slot></slot></div>
    `,

    props: {
        name: {
            required: true
        },
        selected: {
            default: false
        },
    },

    data() {
        return {
            isActive: false
        }
    },

    computed: {
        href() {
            return '#' + this.name.toLowerCase().replace(/ /g, '-')
        }
    },

    mounted() {
        this.isActive = this.selected
    }

});

var vm = new Vue({
    el: '#root',
    delimiters: ['[[', ']]'],
    data: {
        cur: 0,
        items: [{
            "id": 10,
            "labels": [{
                "text": "Prefecture",
                "prob": 0.98
            }],
            "text": 'document'
        }],
        labels: [],
        file: null,
        file_name: '',
    },

    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
            console.log(this.file);
            console.log(this.file.name);
            this.file_name = this.file.name;
        },
        submitFile() {
            let formData = new FormData();
            formData.append('file', this.file);
            axios.post('/' + base_url + '/apis/raw_data',
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(function () {
                    console.log('SUCCESS!!');
                })
                .catch(function () {
                    console.log('FAILURE!!');
                });
        },
        addLabel: function (label) {
            var label = {
                'text': label,
                'prob': null
            };
            this.items[this.cur]['labels'].push(label);

            var label2id = swap(this.labels);
            var data = {
                'id': this.items[this.cur]['id'],
                'label_id': label2id[label['text']]
            };

            axios.post('/' + base_url + '/apis/data', data)
                .then(function (response) {
                    console.log('post data');
                })
                .catch(function (error) {
                    console.log('ERROR!! happend by Backend.')
                });
        },
        deleteLabel: function (index) {
            var label2id = swap(this.labels);
            var label = this.items[this.cur]['labels'][index];
            var payload = {
                'id': this.items[this.cur]['id'],
                'label_id': label2id[label['text']]
            };

            axios.delete('/' + base_url + '/apis/data', {
                    data: payload
                })
                .then(function (response) {
                    console.log('delete data');
                })
                .catch(function (error) {
                    console.log('ERROR!! happend by Backend.')
                });
            this.items[this.cur]['labels'].splice(index, 1)
        },
        submit: function () {
            console.log('submit' + this.searchQuery);
            var self = this;
            axios.get('/' + base_url + '/apis/search?keyword=' + this.searchQuery)
                .then(function (response) {
                    console.log('search response');
                    self.history = response.data['data'];
                })
                .catch(function (error) {
                    console.log('ERROR!! happend by Backend.')
                });
        }
    },
    created: function () {
        var self = this;
        axios.get('/' + base_url + '/apis/labels')
            .then(function (response) {
                self.labels = response.data['labels'];
            })
            .catch(function (error) {
                console.log('ERROR!! happend by Backend.')
            });
    }
});