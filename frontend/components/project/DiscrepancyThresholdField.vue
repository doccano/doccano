<template>
  <v-text-field
    :value="value"
    :label="label"
    :rules="rules"
    :outlined="outlined"
    type="number"
    min="0"
    max="100"
    step="0.1"
    suffix="%"
    persistent-hint
    :hint="hint"
    @input="$emit('input', $event === '' ? '' : parseFloat($event))"
  />
</template>

<script>
export default {
  props: {
    value: {
      type: [Number, String],
      default: ''
    },
    outlined: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      label: 'Percentagem Mínima de Discrepância de Labels',
      hint: 'Defina a percentagem mínima de discrepância para análise comparativa (0-100%)',
      rules: [
        v => (v !== null && v !== undefined && v !== '') || 'Percentagem é obrigatória',
        v => (v === '' || v >= 0) || 'Percentagem deve ser pelo menos 0%',
        v => (v === '' || v <= 100) || 'Percentagem não pode exceder 100%',
        v => (v === '' || !isNaN(parseFloat(v))) || 'Valor deve ser um número válido'
      ]
    }
  }
}
</script> 