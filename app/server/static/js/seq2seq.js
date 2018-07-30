import Vue from 'vue';
Vue.use(require('vue-shortkey'));
import annotationMixin from './mixin.js';
import HTTP from './http.js';

// localStorage persistence
var STORAGE_KEY = 'todos-vuejs-2.0'
var todoStorage = {
    fetch: function () {
        var todos = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
        todos.forEach(function (todo, index) {
            todo.id = index
        })
        todoStorage.uid = todos.length
        return todos
    },
    save: function (todos) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(todos))
    }
}

var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    data: {
        todos: todoStorage.fetch(),
        newTodo: '',
        editedTodo: null
    },
    mixins: [annotationMixin],
    directives: {
        'todo-focus': function (el, binding) {
            if (binding.value) {
                el.focus()
            }
        }
    },
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
        },
        addTodo: function () {
            var value = this.newTodo && this.newTodo.trim()
            if (!value) {
                return
            }
            this.todos.push({
                id: todoStorage.uid++,
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
        }
    },
    created: function () {
        this.updateProgress();
        this.submit();
    },
    watch: {
        todos: {
            handler: function (todos) {
                todoStorage.save(todos)
            },
            deep: true
        }
    }
});