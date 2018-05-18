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
        items: [ //[],
            {
                "id": 10,
                "labels": [{
                    "text": "Prefecture",
                    "prob": 0.98
                }, {
                    "text": "Domestic Region",
                    "prob": 0.58
                }],
                "text": 'Hokkaido, formerly known as Ezo, Yezo, Yeso, or Yesso, is the second largest island of Japan, and the largest and northernmost prefecture. The Tsugaru Strait separates Hokkaido from Honshu.[1] The two islands are connected by the undersea railway Seikan Tunnel. The largest city on Hokkaido is its capital, Sapporo, which is also its only ordinance-designated city. About 43 km north of Hokkaido lies Sakhalin Island, Russia, whereas to its east and north-east are the disputed Kuril Islands.'
            }
        ],
        labels: [{
            'text': 'Prefecture'
        }, {
            'text': 'Organization'
        }, {
            'text': 'Domestic Region'
        }, {
            'text': 'Location'
        }, {
            'text': 'Money'
        }, {
            'text': 'Other'
        }],
        guideline: 'Here is the Annotation Guideline Text'
    },

    methods: {
        addLabel: function (label) {
            var label = {
                'text': label,
                'prob': null
            };
            this.items[this.cur]['labels'].push(label);
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
    }
});