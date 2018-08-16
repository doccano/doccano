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
      text: 'If it had not been for his help, I would have failed.',
    },
    {
      id: 10,
      text: 'According to this magazine, my favorite actress will marry a jazz musician next spring.',
    },
    {
      id: 11,
      text: "It's not always possible to eat well when you are traveling in this part of the world.",
    },
    {
      id: 12,
      text: "It's still early. We should all just chill for a bit.",
    },
    {
      id: 13,
      text: "She got a master's degree three years ago.",
    },
    {
      id: 13,
      text: 'We adopted an alternative method.',
    },
    ],
    annotations: [
      [
        {
          id: 1,
          text: "S'il ne m'avait pas aidé, j'aurais échoué.",
        },
        {
          id: 2,
          text: "S'il ne m'avait pas aidée, j'aurais échoué.",
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
