<template>
  <layout-text v-if="doc.id">
    <template v-slot:header>
      <toolbar-laptop
        :doc-id="doc.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="doc.isConfirmed"
        :show-approve-button="project.permitApprove"
        :total="docs.count"
        class="d-none d-sm-block"
        @click:clear-label="clear"
        @click:review="confirm"
      />
      <toolbar-mobile
        :total="docs.count"
        class="d-flex d-sm-none"
      />
    </template>
    <template v-slot:content>
      <v-card>
        <v-card-text class="title">
          <entity-item-box
            :labels="labels"
            :link-types="linkTypes"
            :text="doc.text"
            :entities="annotations"
            :delete-annotation="remove"
            :update-entity="update"
            :add-entity="add"
            :source-chunk="sourceChunk"
            :source-link-type="sourceLinkType"
            :select-source="selectSource"
            :select-target="selectTarget"
            :delete-link="deleteLink"
            :select-new-link-type="selectNewLinkType"
            :hide-all-link-menus="hideAllLinkMenus"
          />
        </v-card-text>
      </v-card>
    </template>
    <template v-slot:sidebar>
      <list-metadata :metadata="doc.meta" />
    </template>
  </layout-text>
</template>

<script>
import _ from 'lodash'
import {mapGetters} from 'vuex'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import EntityItemBox from '~/components/tasks/sequenceLabeling/EntityItemBox'

const NONE = {
  id: -1,
  none: true
};

export default {
  layout: 'workspace',

  components: {
    EntityItemBox,
    LayoutText,
    ListMetadata,
    ToolbarLaptop,
    ToolbarMobile
  },

  async fetch() {
    this.docs = await this.$services.example.fetchOne(
      this.projectId,
      this.$route.query.page,
      this.$route.query.q,
      this.$route.query.isChecked
    )
    const doc = this.docs.items[0]
    if (this.enableAutoLabeling) {
      await this.autoLabel(doc.id)
    }
    await this.list(doc.id)
  },

  data() {
    return {
      annotations: [],
      docs: [],
      labels: [],
      links: [],
      linkTypes: [],
      project: {},
      enableAutoLabeling: false,
      sourceChunk: NONE,
      sourceLink: NONE,
      sourceLinkType: NONE
    }
  },

  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'getUsername', 'getUserId']),

    shortKeys() {
      return Object.fromEntries(this.labels.map(item => [item.id, [item.suffixKey]]))
    },
    projectId() {
      return this.$route.params.id
    },
    doc() {
      if (_.isEmpty(this.docs) || this.docs.items.length === 0) {
        return {}
      } else {
        return this.docs.items[0]
      }
    }
  },

  watch: {
    '$route.query': '$fetch',
    enableAutoLabeling(val) {
      if (val) {
        this.list(this.doc.id)
      }
    }
  },

  async created() {
    this.labels = await this.$services.label.list(this.projectId)

    this.linkTypes = await this.$services.linkTypes.list(this.projectId)

    this.project = await this.$services.project.findById(this.projectId)
  },

  methods: {
    async list(docId) {
      this.hideAllLinkMenus();

      const annotations = await this.$services.sequenceLabeling.list(this.projectId, docId);
      const links = await this.$services.sequenceLabeling.listLinks(this.projectId);

      annotations.forEach(function(annotation) {
        annotation.links = links.filter(link => link.annotation_id_1 === annotation.id);
      });

      this.annotations = annotations;
      this.links = links;
    },

    populateLinks() {
      const links = this.links;
      this.annotations.forEach(function(annotation) {
        annotation.links = links.filter(link => link.annotation_id_1 === annotation.id);
      });
    },

    async remove(id) {
      this.hideAllLinkMenus();
      await this.$services.sequenceLabeling.delete(this.projectId, this.doc.id, id)
      await this.list(this.doc.id)
    },

    async add(startOffset, endOffset, labelId) {
      this.hideAllLinkMenus();
      await this.$services.sequenceLabeling.create(this.projectId, this.doc.id, labelId, startOffset, endOffset)
      await this.list(this.doc.id)
    },

    async update(labelId, annotationId) {
      this.hideAllLinkMenus();
      await this.$services.sequenceLabeling.changeLabel(this.projectId, this.doc.id, annotationId, labelId)
      await this.list(this.doc.id)
    },

    async clear() {
      await this.$services.sequenceLabeling.clear(this.projectId, this.doc.id)
      await this.list(this.doc.id)
    },

    async autoLabel(docId) {
      try {
        await this.$services.sequenceLabeling.autoLabel(this.projectId, docId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async confirm() {
      await this.$services.example.confirm(this.projectId, this.doc.id)
      await this.$fetch()
    },

    selectSource(chunk) {
      this.sourceChunk = chunk;
    },

    async selectTarget(chunk) {
      // to avoid duplicated links:
      if (!chunk.links.find(ch => ch.id === this.sourceChunk.id)) {
        await this.$services.sequenceLabeling.createLink(this.projectId, this.sourceChunk.id, chunk.id, this.sourceLinkType.id, this.getUserId);
        await this.list(this.doc.id);
      }
      this.hideAllLinkMenus();
    },

    async deleteLink(id, ndx) {
      await this.$services.sequenceLabeling.deleteLink(this.projectId, this.sourceChunk.links[ndx].id)
      await this.list(this.doc.id)

      this.hideAllLinkMenus();
    },

    selectNewLinkType(type) {
      this.sourceLinkType = type;
    },

    hideAllLinkMenus() {
      this.sourceChunk = NONE;
      this.sourceLinkType = NONE;
    }
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  }
}
</script>
