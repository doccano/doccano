<template>
  <v-card>
    <v-card-title>
      <!--
      <member-addition-button />
      <member-deletion-button />
      -->
    </v-card-title>
    <label-list />
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
              <Modal
                ref="childDialogue"
                :title="addModal.title"
                :button="addModal.button"
              >
                <v-text-field
                  label="Label name"
                  prepend-icon="label"
                />
                <v-select
                  :items="keys"
                  label="Key"
                  prepend-icon="mdi-keyboard"
                />
                <v-color-picker
                  v-model="color"
                  show-swatches
                  hide-mode-switch
                  width="800"
                  :mode.sync="mode"
                  class="ma-2"
                />
              </Modal>
              <Modal
                ref="removeDialogue"
                :title="removeModal.title"
                :button="removeModal.button"
              >
                Are you sure you want to remove these labels from this project?
                <v-list dense>
                  <v-list-item v-for="(label, i) in selected" :key="i">
                    <v-list-item-content>
                      <v-list-item-title>{{ label.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </Modal>
            </v-card-title>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
  -->
</template>

<script>
import LabelList from '@/components/containers/LabelList'

export default {
  layout: 'project',
  components: {
    LabelList
  },
  validate({ params }) {
    return /^\d+$/.test(params.id)
  }
}
</script>
