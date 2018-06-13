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
        history: []
    },

    methods: {
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
        nextPage: function () {
            this.cur = Math.min(this.cur + 1, this.items.length - 1);
            this.remaining -= 1;
            console.log('nextPage');
            this.showMessage(this.cur);
        },
        prevPage: function () {
            this.cur = Math.max(this.cur - 1, 0);
            this.remaining += 1;
            this.showMessage(this.cur);
        },
        activeLearn: function () {
            alert('Active Learning!');
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
        },
        showMessage: function (index) {
            this.cur = index;
            console.log(this.cur);
            console.log(this.items[index]);
            $('#message-pane').removeClass('is-hidden');
            $('.card').removeClass('active');
            $('#msg-card-' + index).addClass('active');
            //$('.message .address .name').text(msg.from);
            //$('.message .address .email').text(msg.email);
            var text = this.items[index].text;
            var msg_body = '<p>' + text + '</p>';
            $('.message .content').html(msg_body);
        }
    },
    created: function () {
        var self = this;
        axios.get('/' + base_url + '/apis/labels')
            .then(function (response) {
                self.labels = response.data['labels'];
                //self.total = response.data['total'];
                //self.remaining = response.data['remaining'];
            })
            .catch(function (error) {
                console.log('ERROR!! happend by Backend.')
            });

        axios.get('/' + base_url + '/apis/progress')
            .then(function (response) {
                self.total = response.data['total'];
                self.remaining = response.data['remaining'];
            })
            .catch(function (error) {
                console.log('ERROR!! happend by Backend.')
            });

        axios.get('/' + base_url + '/apis/data')
            .then(function (response) {
                self.items = response.data['data'];
            })
            .catch(function (error) {
                console.log('ERROR!! happend by Backend.')
            });
    },
    computed: {
        done: function () {
            return this.total - this.remaining
        }
    }
});