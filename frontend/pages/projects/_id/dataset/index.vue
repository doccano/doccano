<template>
  <v-card>
    <v-card-title>
    <!--
      <label-creation-button />
      <label-deletion-button />
      -->
    </v-card-title>
    <document-list />
  </v-card>
  <!--
  <v-content>
    <v-container
      fluid
      fill-height
    >
      <v-layout
        justify-center
      >
        <v-flex>
          <v-card>
            <v-card-title>
              <v-btn
                class="mb-2 text-capitalize"
                outlined
                :disabled="selected.length === 0"
                @click="openRemoveModal"
              >
                Remove
              </v-btn>
              <Modal
                ref="removeDialogue"
                :title="removeModal.title"
                :button="removeModal.button"
              >
                Are you sure you want to remove these documents from this project?
                <v-list dense>
                  <v-list-item v-for="(doc, i) in selected" :key="i">
                    <v-list-item-content>
                      <v-list-item-title>{{ doc.text | truncate(50) }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </Modal>
            </v-card-title>
            <v-data-table
              v-model="selected"
              :headers="headers"
              :items="docs"
              item-key="id"
              :search="search"
              show-select
            >
              <template v-slot:top>
                <v-text-field
                  v-model="search"
                  prepend-inner-icon="search"
                  label="Search"
                  single-line
                  hide-details
                  filled
                />
              </template>
              <template v-slot:item.text="{ item }">
                <v-edit-dialog
                  :return-value.sync="item.text"
                  large
                >
                  <span class="d-flex d-sm-none">{{ item.text | truncate(50) }}</span>
                  <span class="d-none d-sm-flex">{{ item.text | truncate(200) }}</span>
                  <template v-slot:input>
                    <v-textarea
                      v-model="item.text"
                      label="Edit"
                    />
                  </template>
                </v-edit-dialog>
              </template>
            </v-data-table>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
  -->
</template>

<script>
import DocumentList from '@/components/containers/DocumentList'
// import DocumentCreationButton from '@/components/containers/DocumentCreationButton'
// import DocumentDeletionButton from '@/components/containers/DocumentDeletionButton'

export default {
  layout: 'project',
  components: {
    DocumentList
    // LabelCreationButton,
    // LabelDeletionButton
  },
  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
