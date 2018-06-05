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
        todos: [],
        labels: [],
        file: null,
        file_name: '',
        newTodo: '',
        editedTodo: null,
    },

    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
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
        addTodo: function () {
            var value = this.newTodo && this.newTodo.trim();
            if (!value) {
                return
            }
            this.todos.push({
                title: value,
            })
            this.newTodo = ''
        },
        removeTodo: function (todo) {
            this.todos.splice(this.todos.indexOf(todo), 1)
        },

        editTodo: function (todo) {
            this.beforeEditCache = todo.title
            this.editedTodo = todo
        },
        doneEdit: function (todo) {
            if (!this.editedTodo) {
                return
            }
            this.editedTodo = null
            todo.title = todo.title.trim()
            if (!todo.title) {
                this.removeTodo(todo)
            }
        },
        cancelEdit: function (todo) {
            this.editedTodo = null
            todo.title = this.beforeEditCache
        },
    },
    created: function () {
        var self = this;
        axios.get('/' + base_url + '/apis/labels')
            .then(function (response) {
                self.labels = response.data['labels'];
                console.log(self.labels);
            })
            .catch(function (error) {
                console.log('ERROR!! happend by Backend.')
            });
    },
    directives: {
        'todo-focus': function (el, binding) {
            if (binding.value) {
                el.focus()
            }
        }
    }
});