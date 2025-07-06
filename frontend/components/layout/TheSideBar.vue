<template>
  <v-list dense>
    <!-- Project Status Indicator -->
    <div class="ma-2 mb-3">
      <v-card 
        :color="project.is_open ? 'success' : 'warning'"
        dark
        elevation="0"
        class="pa-2 text-center"
        style="border-radius: 8px;"
      >
        <div class="d-flex align-center justify-center">
          <v-icon small class="mr-1">
            {{ (project.isOpen !== undefined ? project.isOpen : true) ? 'mdi-lock-open' : 'mdi-lock' }}
          </v-icon>
          <span class="text-caption font-weight-bold">
            {{ (project.isOpen !== undefined ? project.isOpen : true) ? 'OPEN' : 'CLOSED' }}
          </span>
          <v-chip 
            small 
            class="ml-2" 
            :color="(project.isOpen !== undefined ? project.isOpen : true) ? 'success darken-2' : 'warning darken-2'"
            dark
          >
            v{{ project.currentVersion || 1 }}
          </v-chip>
        </div>
        <div class="text-caption mt-1" style="opacity: 0.9;">
          <span v-if="project.isOpen !== undefined ? project.isOpen : true">
            {{ (project.currentVersion || 1) > 1 ? 'Re-annotation Phase' : 'Annotation Phase' }}
          </span>
          <span v-else>
            Discussion & Voting Phase
          </span>
        </div>
      </v-card>
    </div>

    <v-btn 
      color="ms-4 my-1 mb-2 primary text-capitalize" 
      nuxt 
      :disabled="!(project.isOpen !== undefined ? project.isOpen : true)"
      @click="toLabeling"
    >
      <v-icon left>
        {{ mdiPlayCircleOutline }}
      </v-icon>
      {{ $t('home.startAnnotation') }}
    </v-btn>
    
    <!-- Disabled annotation message -->
    <div v-if="!(project.isOpen !== undefined ? project.isOpen : true)" class="text-caption text-center text--secondary ma-2 mb-3">
      Annotation disabled while project is closed
    </div>

    <v-list-item-group v-model="selected" mandatory>
      <v-list-item
        v-for="(item, i) in filteredItems"
        :key="i"
        @click="$router.push(localePath(`/projects/${$route.params.id}/${item.link}`))"
      >
        <v-list-item-action>
          <v-icon>
            {{ item.icon }}
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            {{ item.text }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
import {
  mdiAccount,
  mdiBookOpenOutline,
  mdiCog,
  mdiCommentAccountOutline,
  mdiDatabase,
  mdiHome,
  mdiLabel,
  mdiPlayCircleOutline,
  mdiChatOutline, 
  mdiAlertCircleOutline,
  mdiRobotOutline,
  mdiFileDocumentOutline,
  mdiEyeOutline,
  mdiVote,
  mdiFileChartOutline,
  mdiCompareHorizontal,
  mdiFileDocumentMultiple
} from '@mdi/js'
import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'

export default {
  props: {
    isProjectAdmin: {
      type: Boolean,
      default: false,
      required: true
    },
    project: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  data() {
    return {
      selected: 0,
      mdiPlayCircleOutline,
      mdiVote
    }
  },

  computed: {
    filteredItems() {
      const items = [
        {
          icon: mdiHome,
          text: this.$t('projectHome.home'),
          link: '',
          isVisible: true
        },
        {
          icon: mdiDatabase,
          text: this.$t('dataset.dataset'),
          link: 'dataset',
          isVisible: true
        },
        {
          icon: mdiLabel,
          text: this.$t('labels.labels'),
          link: 'labels',
          isVisible:
            (this.isProjectAdmin || this.project.allowMemberToCreateLabelType) &&
            this.project.canDefineLabel
        },
        {
          icon: mdiLabel,
          text: 'Relations',
          link: 'links',
          isVisible:
            (this.isProjectAdmin || this.project.allowMemberToCreateLabelType) &&
            this.project.canDefineRelation
        },
        {
          icon: mdiAccount,
          text: this.$t('members.members'),
          link: 'members',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiCommentAccountOutline,
          text: 'Comments',
          link: 'comments',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiBookOpenOutline,
          text: this.$t('guideline.guideline'),
          link: 'guideline',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiFileChartOutline,
          text: 'Statistics',
          link: 'statistics',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiChatOutline, // ÍCONE DE CHAT
          text: 'Discussão de Critérios',
          link: 'discussions', // LEVA PARA /projects/:id/discussions
          isVisible: true
        },
        {
          icon: mdiAlertCircleOutline, // ÍCONE DE DISCREPÂNCIAS
          text: 'Discrepancies',
          link: 'discrepancies', // LEVA PARA /projects/:id/discrepancies
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiCompareHorizontal, // ÍCONE DE COMPARAÇÃO
          text: 'Compare Annotations',
          link: 'compare-annotations', // LEVA PARA /projects/:id/compare-annotations
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiRobotOutline, // ÍCONE DE DISCREPÂNCIAS AUTOMÁTICAS
          text: 'Automatic Discrepancies',
          link: 'automatic-discrepancies', // LEVA PARA /projects/:id/automatic-discrepancies
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiFileDocumentOutline, // ÍCONE DE RELATÓRIO DE DESACORDOS
          text: 'Disagreements Report',
          link: 'disagreements-report', // LEVA PARA /projects/:id/disagreements-report
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiEyeOutline,
          text: 'Perspectives',
          link: 'perspectives',
          isVisible: true
        },
        {
          icon: mdiVote,
          text: 'Voting',
          link: 'voting',
          isVisible: true
        },
        {
          icon: mdiFileDocumentMultiple,
          text: 'Versions Report',
          link: 'versions-report',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiCog,
          text: this.$t('settings.title'),
          link: 'settings',
          isVisible: this.isProjectAdmin
        }
      ]
      return items.filter((item) => item.isVisible)
    }
  },

  methods: {
    toLabeling() {
      const query = this.$services.option.findOption(this.$route.params.id)
      const link = getLinkToAnnotationPage(this.$route.params.id, this.project.projectType)
      this.$router.push({
        path: this.localePath(link),
        query
      })
    }
  }
}
</script>
