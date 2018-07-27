import Vue from 'vue';

var vm = new Vue({
    el: '#projects_root',
    delimiters: ['[[', ']]'],
    data: {
        items: [],
        selectedType: 'All'
    },
    methods: {
        get_projects: async function () {
            var base_url = window.location.href.split('/').slice(0, 3).join('/');
            await axios.get(`${base_url}/api/projects`).then(response => {
                this.items = response.data;
            })
        },
        updateSelectedType: function (type) {
            this.selectedType = type;
        }
    },
    computed: {
        uniqueProjectTypes: function () {
            var types = [];
            for (var item of this.items) {
                types.push(item.project_type)
            }
            var uniqueTypes = Array.from(new Set(types));

            return uniqueTypes
        },
        filteredProjects: function () {
            // filter projects
            var projects = [];
            for (var item of this.items) {
                if ((this.selectedType == 'All') || (item.project_type == this.selectedType)) {
                    projects.push(item)
                }
            }
            // create nested projects
            var nested_projects = [];
            for (var i = 0; i < projects.length % 3; i++) {
                var p = projects.slice(i * 3, (i + 1) * 3);
                nested_projects.push(p);
            }

            return nested_projects
        }
    },
    created: function () {
        this.get_projects();
    }
});