import Vue from 'vue';
import annotationMixin from './demo_mixin';

Vue.use(require('vue-shortkey'));


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    newTodo: '',
    editedTodo: null,
    docs: [{
      id: 1,
      text: 'This is a document for named entity recognition.',
    },
    {
      id: 10,
      text: 'This is a sentence.',
    },
    {
      id: 11,
      text: 'This is a sentence.',
    },
    {
      id: 12,
      text: 'This is a sentence.',
    },
    {
      id: 13,
      text: 'This is a sentence.',
    },
    {
      id: 13,
      text: 'This is a sentence.',
    },
    ],
    annotations: [
      [
        {
          id: 1,
          text: 'hotdog',
        },
      ],
      [],
      [],
      [],
      [],
      [],
    ],
  },
  mixins: [annotationMixin],
  directives: {
    'todo-focus': function(el, binding) {
      if (binding.value) {
        el.focus();
      }
    },
  },

  methods: {
    addTodo() {
      const value = this.newTodo && this.newTodo.trim();
      if (!value) {
        return;
      }

      const payload = {
        text: value,
        id: this.annotationId++,
      };
      this.annotations[this.pageNumber].push(payload);

      this.newTodo = '';
    },

    removeTodo(todo) {
      const index = this.annotations[this.pageNumber].indexOf(todo);
      this.annotations[this.pageNumber].splice(index, 1);
    },

    editTodo(todo) {
      this.beforeEditCache = todo.text;
      this.editedTodo = todo;
    },

    doneEdit(todo) {
      if (!this.editedTodo) {
        return;
      }
      this.editedTodo = null;
      todo.text = todo.text.trim();
      if (!todo.text) {
        this.removeTodo(todo);
      }
    },

    cancelEdit(todo) {
      this.editedTodo = null;
      todo.text = this.beforeEditCache;
    },
  },
});
