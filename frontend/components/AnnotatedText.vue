<template>
  <div class="annotated-text-container">
    <span
      v-for="(part, index) in annotatedParts"
      :key="index"
      :class="{
        'annotated-span': part.isAnnotated,
        [part.className]: part.isAnnotated,
        'discrepant-span': part.isDiscrepant // Adiciona classe se for discrepante
      }"
      :style="{
        backgroundColor: part.color,
        color: 'black' // Texto preto para contraste com as cores vibrantes
      }"
    >
      {{ part.text }}
    </span>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

type SpanAnnotation = {
  label: string; // Assumindo que você terá o nome do label aqui
  start_offset: number;
  end_offset: number;
  isDiscrepant?: boolean; // Nova propriedade para marcar discrepância
}

// Tipo para Label (não é mais necessário aqui, mas mantido por referência)
// type Label = {
//   id: number
//   text: string
//   shortcut: string | null
//   background_color: string
//   text_color: string
// }

export default Vue.extend({
  name: 'AnnotatedText',
  props: {
    text: {
      type: String,
      required: true
    },
    annotations: {
      type: Array as () => SpanAnnotation[],
      default: () => []
    },
    labelColors: {
      type: Object as () => { [key: string]: string },
      required: true
    }
  },
  data() {
    return {
      // labelColors não é mais necessário localmente
    }
  },
  computed: {
    annotatedParts(): Array<{ text: string; isAnnotated: boolean; className?: string; color?: string; isDiscrepant?: boolean }> {
      const parts: Array<{ text: string; isAnnotated: boolean; className?: string; color?: string; isDiscrepant?: boolean }> = []
      let lastIndex = 0
      const sortedAnnotations = [...this.annotations].sort((a, b) => a.start_offset - b.start_offset)

      sortedAnnotations.forEach(annotation => {
        if (annotation.start_offset > lastIndex) {
          parts.push({
            text: this.text.substring(lastIndex, annotation.start_offset),
            isAnnotated: false
          })
        }

        const color = this.labelColors[annotation.label] || '#FFF';

        parts.push({
          text: this.text.substring(annotation.start_offset, annotation.end_offset),
          isAnnotated: true,
          className: `label-${annotation.label.toLowerCase().replace(/[^a-z0-9]/g, '')}`,
          color,
          isDiscrepant: annotation.isDiscrepant // Passar o flag de discrepância da anotação
        })
        lastIndex = annotation.end_offset
      })

      if (lastIndex < this.text.length) {
        parts.push({
          text: this.text.substring(lastIndex),
          isAnnotated: false
        })
      }

      return parts
    }
  },
  methods: {
    // getLabelColor não é mais necessário
  }
})
</script>

<style scoped>
.annotated-text-container {
  /* white-space: pre-wrap; */ /* Removido para permitir quebra de linha normal */
  /* word-wrap: break-word; */ /* Removido para permitir quebra de linha normal */
  font-size: 1.4em; /* Aumenta o tamanho da fonte para melhor legibilidade */
  line-height: 1.4; /* Melhora o espaçamento entre linhas */
}

.annotated-span {
  padding: 0 2px; /* Ajustado para melhor visualização */
  border-radius: 3px;
  /* opacity: 0.8; */ /* Removido para garantir que as cores apareçam */
  display: inline-block; /* Garante que o padding e background funcionem bem em linha */
  white-space: normal; /* Garante que o texto dentro do span quebre normalmente */
}

/* A classe .label-text não é mais necessária, pois o texto do label foi removido */
/* .label-text {
  font-size: 0.7em;
  vertical-align: super;
  margin-left: 3px;
  opacity: 0.7;
} */

.discrepant-span {
  border: none; /* Remover a borda */
  text-decoration: underline red; /* Sublinhar em vermelho */
  opacity: 1; /* Garante que a discrepância seja visível */
}
</style> 