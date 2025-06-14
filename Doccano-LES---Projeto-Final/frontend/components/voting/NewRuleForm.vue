<template>
  <v-card outlined class="mt-4">
    <v-card-title class="subtitle-1">
      Criar Nova Regra
    </v-card-title>
    
    <v-card-text>
      <v-form ref="form">
        <v-text-field
          v-model="ruleName"
          label="Nome da Regra"
          :rules="[v => !!v || 'Nome é obrigatório']"
          required
          clearable
        />

        <v-textarea
          v-model="ruleDescription"
          label="Descrição"
          :rules="[v => !!v || 'Descrição é obrigatória']"
          rows="3"
          required
          clearable
          class="mt-4"
        />

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="secondary"
            text
            @click="$emit('cancel')"
          >
            Cancelar
          </v-btn>
          <v-btn
            :loading="saving"
            color="primary"
            :disabled="!isFormValid"
            @click="saveRule"
          >
            Salvar
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'

export default defineComponent({
  name: 'NewRuleForm',
  
  emits: ['cancel', 'save'],
  
  setup(_, { emit }) {
    const form = ref(null)
    const ruleName = ref('')
    const ruleDescription = ref('')
    const saving = ref(false)

    const isFormValid = computed(() => {
      return ruleName.value && ruleDescription.value
    })

    const saveRule = () => {
      if (!form.value.validate()) {
        return
      }

      saving.value = true
      try {
        emit('save', {
          name: ruleName.value,
          description: ruleDescription.value
        })

        // Limpar formulário
        ruleName.value = ''
        ruleDescription.value = ''
      } finally {
        saving.value = false
      }
    }

    return {
      form,
      ruleName,
      ruleDescription,
      saving,
      isFormValid,
      saveRule
    }
  }
})
</script>

<style scoped>
.new-rule-form {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}
</style> 