<template lang="pug">
  div(v-cloak="")
    section.hero.project-image
      div.container
        div.columns
          div.column.is-10.is-offset-1

            h1.title.is-1.has-text-white Hello, {{ username | title }}.
            h2.subtitle.is-4.has-text-white I hope you are having a great day!

            p(v-if="isSuperuser")
              a.button.is-medium.is-primary(v-on:click="isActive = !isActive") Create Project

    div.modal(v-bind:class="{ 'is-active': isActive }")
      div.modal-background
      div.modal-card
        header.modal-card-head
          p.modal-card-title Create Project
          button.delete(aria-label="close", v-on:click="isActive = !isActive")

        section.modal-card-body
          div.field
            label.label Project Name
            div.control
              input.input(v-model="projectName", type="text", required, placeholder="Project name")
            p.help.is-danger {{ projectNameError }}

          div.field
            label.label Description
            div.control
              textarea.textarea(v-model="description", required, placeholder="Project description")
            p.help.is-danger {{ descriptionError }}

          div.field
            label.label Project Type

            div.control
              select(v-model="projectType", name="project_type", required)
                option(value="", selected="selected") ---------
                option(value="DocumentClassification") document classification
                option(value="SequenceLabeling") sequence labeling
                option(value="Seq2seq") sequence to sequence
            p.help.is-danger {{ projectTypeError }}

          div.field
            label.checkbox
              input(
                v-model="randomizeDocumentOrder"
                name="randomize_document_order"
                type="checkbox"
                style="margin-right: 0.25em;"
                required
              )
              | Randomize document order per user

        footer.modal-card-foot.pt20.pb20.pr20.pl20.has-background-white-ter
          button.button.is-primary(v-on:click="create()") Create
          button.button(v-on:click="isActive = !isActive") Cancel

    div.modal(v-bind:class="{ 'is-active': isDelete }")
      div.modal-background
      div.modal-card
        header.modal-card-head
          p.modal-card-title Delete Project
          button.delete(aria-label="close", v-on:click="isDelete = !isDelete")
        section.modal-card-body Are you sure you want to delete project?
        footer.modal-card-foot.pt20.pb20.pr20.pl20.has-background-white-ter
          button.button.is-danger(v-on:click="deleteProject()") Delete
          button.button(v-on:click="isDelete = !isDelete") Cancel

    section.hero
      div.container
        div.columns
          div.column.is-10.is-offset-1
            div.card.events-card
              header.card-header
                p.card-header-title {{ items.length }} Projects

                div.field.card-header-icon
                  div.control
                    div.select
                      select(v-model="selected")
                        option(selected) All Project
                        option Text Classification
                        option Sequence Labeling
                        option Seq2seq

              div.card-table
                div.content
                  table.table.is-fullwidth
                    tbody
                      tr(v-for="project in selectedProjects", v-bind:key="project.id")
                        td.pl15r
                          div.thumbnail-wrapper.is-vertical
                            img.project-thumbnail(
                              v-bind:src="project.image"
                              alt="Project thumbnail"
                            )

                          div.dataset-item__main.is-vertical
                            div.dataset-item__main-title
                              div.dataset-item__main-title-link.dataset-item__link
                                a.has-text-black(v-bind:href="'/projects/' + project.id")
                                  | {{ project.name }}

                            div.dataset-item__main-subtitle {{ project.description }}
                            div.dataset-item__main-info
                              span.dataset-item__main-update updated
                                span {{ project.updated_at | daysAgo }}

                        td.is-vertical
                          span.tag.is-normal {{ project.project_type }}

                        td.is-vertical(v-if="isSuperuser")
                          a(v-bind:href="'/projects/' + project.id + '/docs'") Edit

                        td.is-vertical(v-if="isSuperuser")
                          a.has-text-danger(v-on:click="setProject(project)") Delete
</template>

<script>
import { title, daysAgo } from './filter';
import { newHttpClient } from './http';

const baseUrl = window.location.href.split('/').slice(0, 3).join('/');
const httpClient = newHttpClient();

export default {
  filters: { title, daysAgo },

  data: () => ({
    items: [],
    isActive: false,
    isDelete: false,
    project: null,
    selected: 'All Project',
    projectName: '',
    description: '',
    projectType: '',
    descriptionError: '',
    projectTypeError: '',
    projectNameError: '',
    username: '',
    isSuperuser: false,
    randomizeDocumentOrder: false,
  }),

  computed: {
    selectedProjects() {
      return this.items.filter(item => this.selected === 'All Project' || this.matchType(item.project_type));
    },
  },

  created() {
    Promise.all([
      httpClient.get(`${baseUrl}/v1/projects`),
      httpClient.get(`${baseUrl}/v1/me`),
    ]).then(([projects, me]) => {
      this.items = projects.data;
      this.username = me.data.username;
      this.isSuperuser = me.data.is_superuser;
    });
  },

  methods: {
    deleteProject() {
      httpClient.delete(`${baseUrl}/v1/projects/${this.project.id}`).then(() => {
        this.isDelete = false;
        const index = this.items.indexOf(this.project);
        this.items.splice(index, 1);
      });
    },

    setProject(project) {
      this.project = project;
      this.isDelete = true;
    },

    matchType(projectType) {
      if (projectType === 'DocumentClassification') {
        return this.selected === 'Text Classification';
      }
      if (projectType === 'SequenceLabeling') {
        return this.selected === 'Sequence Labeling';
      }
      if (projectType === 'Seq2seq') {
        return this.selected === 'Seq2seq';
      }
      return false;
    },

    create() {
      const payload = {
        name: this.projectName,
        description: this.description,
        project_type: this.projectType,
        randomize_document_order: this.randomizeDocumentOrder,
        guideline: 'Please write annotation guideline.',
        resourcetype: this.resourceType(),
      };
      httpClient.post(`${baseUrl}/v1/projects`, payload)
        .then((response) => {
          window.location = `${baseUrl}/projects/${response.data.id}/docs/create`;
        })
        .catch((error) => {
          this.projectTypeError = '';
          this.projectNameError = '';
          this.descriptionError = '';
          if ('resourcetype' in error.response.data) {
            this.projectTypeError = error.response.data.resourcetype;
          }
          if ('name' in error.response.data) {
            this.projectNameError = error.response.data.name[0];
          }
          if ('description' in error.response.data) {
            this.descriptionError = error.response.data.description[0];
          }
        });
    },

    resourceType() {
      if (this.projectType === 'DocumentClassification') {
        return 'TextClassificationProject';
      }
      if (this.projectType === 'SequenceLabeling') {
        return 'SequenceLabelingProject';
      }
      if (this.projectType === 'Seq2seq') {
        return 'Seq2seqProject';
      }
      return '';
    },
  },
};
</script>
