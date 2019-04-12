<template lang="pug">
extends ../annotation.pug

block annotation-area
  div
    div.card.has-text-weight-bold.has-text-white.has-background-royalblue
      div.card-content
        div.content(v-if="docs[pageNumber]") {{ docs[pageNumber].text }}

    section.todoapp
      header.header
        input.textarea.new-todo(
          type="text",
          placeholder="What is your response?",
          v-model="newTodo",
          @keyup.enter="addTodo"
        )
      section.main(v-cloak="")
        ul.todo-list
          li.todo(
            v-for="todo in annotations[pageNumber]",
            :key="todo.id",
            :class="{ \
              editing: todo == editedTodo \
            }"
          )
            div.view
              label(@dblclick="editTodo(todo)") {{ todo.text }}
              button.delete.destroy.is-large(@click="removeTodo(todo)")

            input.textarea.edit(
              type="text",
              v-model="todo.text",
              v-todo-focus="todo == editedTodo",
              @blur="doneEdit(todo)",
              @keyup.enter="doneEdit(todo)",
              @keyup.esc="cancelEdit(todo)"
            )
</template>

<script>
import annotationMixin from './demo_mixin';
import todoFocus from '../directives';
import { demoTranslation } from './demo_data';

export default {
  directives: { todoFocus },

  mixins: [annotationMixin],

  data: () => ({ ...demoTranslation }),

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
};
</script>
