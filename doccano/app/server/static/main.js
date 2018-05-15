Vue.config.debug = true;

var app4 = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    cur: 2,
    items: [
      {"id": 10, "labels": [{"text": "Prefecture", "prob": 0.98}, {"text": "Domestic Region", "prob": 0.58}], "text": "北海道（ほっかいどう）は、日本の北部に位置する島[※ 1][※ 2]。また、同島および付随する島を管轄する地方公共団体（道）である。島としての北海道は日本列島を構成する主要4島の一つである。地方公共団体としての北海道は47都道府県中唯一の「道」で、道庁所在地は札幌市。"},
      {"id": 11, "labels": [{"text": "Person", "prob": 0.98}], "text": "安倍 晋三（あべ しんぞう、1954年（昭和29年）9月21日 - ）は、日本の政治家。自由民主党所属の衆議院議員（9期）、第90代・第96代・第97代・第98代内閣総理大臣、第21代・第25代自由民主党総裁。"},
      {"id": 12, "labels": [{"text": "Country", "prob": 0.99}, {"text": "Continental Region", "prob": 0.58}], "text": "アメリカ合衆国（アメリカがっしゅうこく、英語: United States of America）、通称アメリカ、米国（べいこく）は、50の州および連邦区から成る連邦共和国である[6][7]。アメリカ本土の48州およびワシントンD.C.は、カナダとメキシコの間の北アメリカ中央に位置する。アラスカ州は北アメリカ北西部の角に位置し、東ではカナダと、西ではベーリング海峡をはさんでロシアと国境を接している。ハワイ州は中部太平洋における島嶼群である。同国は、太平洋およびカリブに5つの有人の海外領土および9つの無人の海外領土を有する。985万平方キロメートル (km2) の総面積は世界第3位または第4位、3億1千7百万人の人口は世界第3位である。同国は世界で最も民族的に多様かつ多文化な国の1つであり、これは多くの国からの大規模な移住の産物とされている[8]。また同国の広大な国土における地理および気候も極めて多様であり、多種多様な野生生物が存在する。"},
    ],
    labels: [],
    guideline: 'annotation text'
  },
  methods: {
    addLabel: function (label) {
        this.items[this.cur]['labels'].push({"text": label, "prob":null})
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
    axios.get('/annotation/api/label')
      .then(function(response) {
        console.log('label request');
        self.labels = response.data['labels'];
    })
    .catch(function(error) {
      console.log('ERROR!! happend by Backend.')
    });
  }
})