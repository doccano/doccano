import Vue from 'vue';
Vue.use(require('vue-shortkey'));
import annotationMixin from './mixin.js';
import HTTP from './http.js';


var vm = new Vue({
    el: '#mail-app',
    delimiters: ['[[', ']]'],
    data: {
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
        addTodo: function () {
            var value = this.newTodo && this.newTodo.trim()
            if (!value) {
                return
            }

            var doc_id = this.items[this.cur].id;
            var payload = {text: value}
            HTTP.post(`docs/${doc_id}/annotations/`, payload).then(response => {
                this.items[this.cur]['labels'].push(response.data)
            })

            this.newTodo = ''
        },

        removeTodo: function (todo) {
            var doc_id = this.items[this.cur].id;
            HTTP.delete(`docs/${doc_id}/annotations/${todo.id}`).then(response => {
                this.items[this.cur]['labels'].splice(this.items[this.cur]['labels'].indexOf(todo), 1)
            });
        },

        editTodo: function (todo) {
            this.beforeEditCache = todo.text
            this.editedTodo = todo
        },

        doneEdit: function (todo) {
            if (!this.editedTodo) {
                return
            }
            this.editedTodo = null
            todo.text = todo.text.trim()
            if (!todo.text) {
                this.removeTodo(todo)
            }
            var doc_id = this.items[this.cur].id;
            HTTP.put(`docs/${doc_id}/annotations/${todo.id}`, todo).then(response => {
                console.log(response)
            });
        },

        cancelEdit: function (todo) {
            this.editedTodo = null
            todo.text = this.beforeEditCache
        }
    },
    created: function () {
        this.updateProgress();
        this.submit();
    }
});