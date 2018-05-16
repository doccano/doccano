Vue.config.debug = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
var base_url = window.location.href.split('/').slice(3, 5).join('/');

function swap(values){
  var ret = {};
  for(var item of values){
    ret[item['text']] = item['id'];
  }
  return ret;
}

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    cur: 0,
    items: [],
//    {
//      "id": 10,
//      "labels": [{
//        "text": "Prefecture",
//        "prob": 0.98
//      }, {
//        "text": "Domestic Region",
//        "prob": 0.58
//      }],
//      "text": "北海道（ほっかいどう）は、日本の北部に位置する島[※ 1][※ 2]。また、同島および付随する島を管轄する地方公共団体（道）である。島としての北海道は日本列島を構成する主要4島の一つである。地方公共団体としての北海道は47都道府県中唯一の「道」で、道庁所在地は札幌市。"
//    }
    labels: [],
    guideline: ''
  },
  methods: {
    addLabel: function (label) {
      var label = {
        'text': label,
        'prob': null
      };
      this.items[this.cur]['labels'].push(label);
      console.log(this.labels);
      console.log(swap(this.labels));
      var label2id = swap(this.labels);
      var data = {'id': this.items[this.cur]['id'], 'label_id': label2id[label['text']]};

      axios.post('/' + base_url + '/apis/data', data)
        .then(function (response) {
          console.log('post data');
        })
        .catch(function (error) {
          console.log('ERROR!! happend by Backend.')
        });
    },
    deleteLabel: function (index) {
      this.items[this.cur]['labels'].splice(index, 1)
    },
    nextPage: function () {
      this.cur += 1
    },
    prevPage: function () {
      this.cur -= 1
    }
  },
  created: function () {
    console.log('created');
    var self = this;
    axios.get('/' + base_url + '/apis/label')
      .then(function (response) {
        console.log('request label');
        self.labels = response.data['labels'];
      })
      .catch(function (error) {
        console.log('ERROR!! happend by Backend.')
      });

    axios.get('/' + base_url + '/apis/data')
      .then(function (response) {
        console.log('request data');
        self.items = response.data['data'];
      })
      .catch(function (error) {
        console.log('ERROR!! happend by Backend.')
      });
  }
})