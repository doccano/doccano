import Vue from 'vue';
Vue.use(require('vue-shortkey'));

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

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    data: {
        cur: 0,
        items: [{
            "id": null,
            "labels": [],
            "text": ''
        }],
        labels: [],
        guideline: 'Here is the Annotation Guideline Text',
        total: 0,
        remaining: 0,
        searchQuery: '',
        hasNext: false,
        hasPrevious: false,
        nextPageNum: 1,
        prevPageNum: 1,
        page: 1,
        message_body: '',
    },

    methods: {
        addLabel: function (label) {
            for (var i = 0; i < this.items[this.cur]['labels'].length; i++) {
              var item = this.items[this.cur]['labels'][i];
              if (label == item.text) {
                this.deleteLabel(i);
                return;
              }
            }

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
            this.updateProgress();
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
            this.updateProgress();
        },
        nextPage: function () {
            this.cur += 1;
            if (this.cur == this.items.length) {
              if (this.hasNext) {
                this.page = this.nextPageNum;
                this.submit();
                this.cur = 0;
              } else {
                this.cur = this.items.length - 1;
              }
            }
            this.showMessage(this.cur);
        },
        prevPage: function () {
            this.cur -= 1;
            if (this.cur == -1) {
              if (this.hasPrevious) {
                this.page = this.prevPageNum;
                this.submit();
                this.cur = this.items.length - 1;
              } else {
                this.cur = 0;
              }
            }
            this.showMessage(this.cur);
        },
        activeLearn: function () {
            alert('Active Learning!');
        },
        submit: function () {
            console.log('submit' + this.searchQuery);
            var self = this;
            axios.get('/' + base_url + '/apis/search?keyword=' + this.searchQuery + '&page=' + this.page)
                .then(function (response) {
                    console.log('search response');
                    console.log(response.data);
                    self.items = response.data['data'];
                    self.hasNext = response.data['has_next']
                    self.nextPageNum = response.data['next_page_number']
                    self.hasPrevious = response.data['has_previous']
                    self.prevPageNum = response.data['previous_page_number']
                    //self.searchQuery = '';
                })
                .catch(function (error) {
                    console.log('ERROR!! happend by Backend.')
                });
        },
        showMessage: function (index) {
            this.cur = index;
            //$('#message-pane').removeClass('is-hidden');
            $('.card').removeClass('active');
            $('#msg-card-' + index).addClass('active');
            var text = this.items[index].text;
            this.message_body = text;
        },
        updateProgress: function() {
            var self = this;
            axios.get('/' + base_url + '/apis/progress')
            .then(function (response) {
                self.total = response.data['total'];
                self.remaining = response.data['remaining'];
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
        this.updateProgress();
        this.submit();
    },
    computed: {
        done: function () {
            return this.total - this.remaining
        },
        achievement: function () {
            if (this.total == 0) {
                return 0;
            } else {
                return (this.total - this.remaining) / this.total * 100
            }
        },
        progressColor: function () {
            if (this.achievement < 30) {
                return 'is-danger'
            } else if (this.achievement < 70) {
                return 'is-warning'
            } else {
                return 'is-primary'
            }
        }
    }
});