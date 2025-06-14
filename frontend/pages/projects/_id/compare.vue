<template>
  <v-card>
    <v-card-title>
      <h2>Comparação de Anotações</h2>
      <v-spacer />
    </v-card-title>
    <v-card-text>
      <div v-if="isLoading">Carregando dados para comparação...</div>
      <div v-else-if="!documentText">Não foi possível carregar o documento ou anotações.</div>
      <div v-else>
        <div class="mb-4">
          <h3>Legenda:</h3>
          <div class="d-flex flex-wrap">
            <div
              v-for="labelName in uniqueLabelsForLegend"
              :key="labelName"
              :style="{ backgroundColor: getLabelColor(labelName), color: 'black', padding: '4px 8px', margin: '4px', borderRadius: '4px' }"
            >
              {{ labelName }}
            </div>
          </div>
        </div>

        <v-row>
          <v-col cols="12" md="6">
            <h4>Anotações do {{ user1Name }}:</h4>
            <div v-if="user1Annotations.length === 0">Nenhuma anotação encontrada para este usuário.</div>
            <div v-else>
              <AnnotatedText :text="documentText" :annotations="user1Annotations" :labelColors="labelColorsDict" />
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <h4>Anotações do {{ user2Name }}:</h4>
            <div v-if="user2Annotations.length === 0">Nenhuma anotação encontrada para este usuário.</div>
            <div v-else>
              <AnnotatedText :text="documentText" :annotations="user2Annotations" :labelColors="labelColorsDict" />
            </div>
          </v-col>
        </v-row>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import AnnotatedText from '@/components/AnnotatedText.vue'

// Tipos para anotações de span
type SpanAnnotation = {
  id?: number
  prob?: number
  user: number
  example?: number
  created_at?: string
  updated_at?: string
  label: string; // Corrigido para string
  start_offset: number
  end_offset: number
}

// Tipo para Label
// type Label = {
//   id: number
//   text: string
//   shortcut: string | null
//   background_color: string
//   text_color: string
// }

export default Vue.extend({
  name: 'AnnotationCompare',

  components: {
    AnnotatedText
  },

  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      isLoading: true,
      projectId: '' as string,
      exampleId: '' as string,
      user1Id: '' as string,
      user2Id: '' as string,
      documentText: '' as string,
      user1Annotations: [] as SpanAnnotation[],
      user2Annotations: [] as SpanAnnotation[],
      user1Name: '' as string,
      user2Name: '' as string,
      discrepancyReport: null as string | null,
      labelColors: {} as { [key: string]: string },
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      this.projectId = this.$route.params.id
      this.exampleId = this.$route.query.exampleId as string
      this.user1Id = this.$route.query.user1Id as string
      this.user2Id = this.$route.query.user2Id as string

      if (!this.projectId || !this.exampleId || !this.user1Id || !this.user2Id) {
        console.error('Parâmetros de rota ausentes.')
        this.isLoading = false
        return
      }

      console.log('this.$repositories:', this.$repositories);
      const [exampleResponse, membersResponse] = await Promise.all([
        this.$repositories.example.findById(this.projectId, parseInt(this.exampleId)),
        this.$repositories.member.list(this.projectId),
      ]);

      this.documentText = exampleResponse.text

      // As anotações (spans) já vêm na resposta do documento
      // Não é mais necessário mapear label ID para nome, pois já vem como string.
      const initialUser1Annotations = exampleResponse.annotations.filter((annotation: any) => annotation.user.toString() === this.user1Id);
      const initialUser2Annotations = exampleResponse.annotations.filter((annotation: any) => annotation.user.toString() === this.user2Id);

      // Marcar discrepâncias nos spans
      const { markedAnnotations1, markedAnnotations2 } = this.markDiscrepantSpans(
        initialUser1Annotations,
        initialUser2Annotations
      );
      this.user1Annotations = markedAnnotations1;
      this.user2Annotations = markedAnnotations2;

      const user1Member = membersResponse.find((m: any) => m.user.toString() === this.user1Id);
      const user2Member = membersResponse.find((m: any) => m.user.toString() === this.user2Id);
      this.user1Name = user1Member ? user1Member.username : `Usuário ${this.user1Id}`;
      this.user2Name = user2Member ? user2Member.username : `Usuário ${this.user2Id}`;

      // this.discrepancyReport = this.compareAnnotations(this.user1Annotations, this.user2Annotations); // Removido: não exibe mais o relatório textual

    } catch (e) {
      console.error('Erro ao buscar dados para comparação:', e)
    } finally {
      this.isLoading = false
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),
    compareAnnotations(): (annotations1: any[], annotations2: any[]) => string | null {
      return (annotations1: any[], annotations2: any[]) => {
        const differences: string[] = []

        const spans1 = annotations1.filter(a => a.start_offset !== undefined).sort((a, b) => a.start_offset - b.start_offset)
        const spans2 = annotations2.filter(a => a.start_offset !== undefined).sort((a, b) => a.start_offset - b.start_offset)

        if (spans1.length !== spans2.length) {
          differences.push(`Número diferente de spans: ${spans1.length} vs ${spans2.length}`)
        } else {
          for (let i = 0; i < spans1.length; i++) {
            if (spans1[i].label !== spans2[i].label ||
                spans1[i].start_offset !== spans2[i].start_offset ||
                spans1[i].end_offset !== spans2[i].end_offset) {
              differences.push(`Span diferente: "${spans1[i].start_offset}-${spans1[i].end_offset}:${spans1[i].label}" vs "${spans2[i].start_offset}-${spans2[i].end_offset}:${spans2[i].label}"`)
            }
          }
        }
        return differences.length > 0 ? differences.join('\n') : null
      }
    },
    uniqueLabelsForLegend(): string[] {
      const allLabels = [
        ...this.user1Annotations.map(ann => ann.label),
        ...this.user2Annotations.map(ann => ann.label),
      ];
      return Array.from(new Set(allLabels));
    },
    labelColorsDict(): { [key: string]: string } {
      // Gera as cores de forma determinística para todos os labels únicos
      // Cores mais claras/pastéis para melhor contraste com sublinhado vermelho
      const colors = [
        '#FFB6C1', // Light Pink
        '#87CEEB', // Sky Blue
        '#98FB98', // Pale Green
        '#F0E68C', // Khaki
        '#DDA0DD', // Plum
        '#AFEEEE', // Pale Turquoise
        '#FFE4E1', // Misty Rose
        '#E0FFFF', // Light Cyan
        '#FFEFD5', // Papaya Whip
        '#F5DEB3', // Wheat
        '#D8BFD8', // Thistle
        '#B0E0E6', // Powder Blue
        '#FAFAD2', // Light Goldenrod Yellow
        '#FFE4B5', // Moccasin
        '#E6E6FA', // Lavender
        '#F0FFFF', // Azure
        '#FFF8DC', // Cornsilk
        '#F5F5DC', // Beige
        '#FFFACD', // Lemon Chiffon
        '#F0F8FF', // Alice Blue
      ];
      const dict: { [key: string]: string } = {};
      this.uniqueLabelsForLegend.forEach(label => {
        const hash = label.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
        dict[label] = colors[hash % colors.length];
      });
      return dict;
    },
  },
  methods: {
    getLabelColor(label: string): string {
      return this.labelColorsDict[label] || '#FFF';
    },
    markDiscrepantSpans(
      annotations1: SpanAnnotation[],
      annotations2: SpanAnnotation[]
    ): { markedAnnotations1: SpanAnnotation[]; markedAnnotations2: SpanAnnotation[] } {
      const markedAnnotations1: SpanAnnotation[] = annotations1.map(ann => ({ ...ann, isDiscrepant: false }))
      const markedAnnotations2: SpanAnnotation[] = annotations2.map(ann => ({ ...ann, isDiscrepant: false }))

      // Função auxiliar para verificar se uma anotação existe em uma lista
      const existsInList = (annotation: SpanAnnotation, list: SpanAnnotation[]) => {
        return list.some(
          a =>
            a.start_offset === annotation.start_offset &&
            a.end_offset === annotation.end_offset &&
            a.label === annotation.label
        )
      }

      // Marcar discrepâncias na primeira lista
      markedAnnotations1.forEach(ann1 => {
        if (!existsInList(ann1, markedAnnotations2)) {
          ann1.isDiscrepant = true
        }
      })

      // Marcar discrepâncias na segunda lista
      markedAnnotations2.forEach(ann2 => {
        if (!existsInList(ann2, markedAnnotations1)) {
          ann2.isDiscrepant = true
        }
      })

      return { markedAnnotations1, markedAnnotations2 }
    }
  }
})
</script>

<style scoped>
/* Estilos futuros para a visualização lado a lado */
</style>