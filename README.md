# Doccano - Extensão para a disciplina de Laboratório de Engenharia de Software

Este projeto foi desenvolvido no âmbito da disciplina de Laboratório de Engenharia de Software, do curso de Engenharia Informática da Faculdade de Ciências e Tecnologia da Universidade do Algarve. Criado pelos estudantes da instituição, este trabalho visa aprimorar e expandir as funcionalidades do Doccano tornando-o assim mais completo e adequado às necessidades do ambiente acadêmico e profissional.

## Visão Geral
Este projeto expande a funcionalidade do [Doccano](https://github.com/doccano/doccano) para incluir novos recursos voltados para a:
- **Gestão de utilizadores**  
- **Gestão de desacordos entre anotadores**  
- **Gestão de perspetivas anotadoras**

Para além destas, visa-se incorporar também recursos adicionais voltados para a:
- **Resolução colaborativa de desacordos**  
- **Geração de relatórios de desacordo e perspetiva**  

Essas melhorias visam tornar o Doccano num ambiente de anotação mais flexível, colaborativo e estatisticamente analisável.

---

## Funcionalidades e Casos de Uso

Para uma melhor organização e compreensão do sistema, as funcionalidades foram divididas em diferentes áreas de gestão.
Cada uma destas áreas aborda aspetos essenciais o que possibilita uma abordagem estruturada e, consequentemente, mais eficiente. 
As principais divisões incluem a gestão de utilizadores, a gestão de desacordos entre anotadores, a gestão de perspetivas anotadoras, a resolução colaborativa de desacordos e a geração de relatórios. 


### **1. Gestão de Utilizadores - 8 casos de uso**
- Criar utilizador.
    - Formulário para inserir nome, e-mail e senha.
    - Escolha de permissões (Admin, Anotador).
    - Validação e criação no banco de dados.
    - Envio de e-mail com credenciais.
- Editar utilizador.
    - Listagem de utilizadores com opção de edição.
    - Alteração de nome, e-mail ou papel no sistema.
    - Atualização no banco de dados.
- Remover utilizador.
    - Botão para exclusão de utilizador.
    - Confirmação antes da remoção.
    - Garantia de que não existem dependências antes da exclusão.
- Consultar utilizadores.
    - Exibição de lista de utilizadores registados.
    - Possibilidade de ordenar por nome, data de criação, papel.
    - Paginação da lista.
- Atribuir permissões e papéis.
    - Menu suspenso com opções de papéis (Admin, Anotador, Convidado).
    - Registo das permissões na base de dados.
    - Restrições para evitar alterações indevidas.
- Alterar permissões de utilizadores.
    - Formulário para modificar permissões existentes.
    - Registo de auditoria sobre as alterações realizadas.
- Reset de senha/autenticação.
    - Opção de redefinição de palavra-passe via e-mail.
    - Geração de link seguro para redefinição.
    - Armazenamento seguro das novas palavras-passe.
- Listagem filtrada de utilizadores.
    - Filtros por nome, papel e estado.
    - Pesquisa por e-mail ou ID.

### **2. Gestão de Desacordos entre Anotadores - 5 casos de uso**
- Identificação automática de discrepâncias entre anotações.
    - Comparação de anotações feitas sobre o mesmo texto.
    - Algoritmo para deteção de diferenças.
    - Registo automático das discrepâncias.
- Sinalização visual de desacordos.
    - Marcação de anotações com conflitos (ex: cor vermelha).
    - Ícones indicando grau de divergência.
    - Mensagens de dica com detalhes da diferença.
- Apresentação lado a lado de anotações divergentes.
    - Interface com colunas separadas para cada anotação.
    - Destaque das diferenças entre versões.
    - Possibilidade de expandir detalhes.
- Permite discussão sobre as diferenças diretamente na interface.
    - Caixa de comentários para cada desacordo.
    - Notificação de novos comentários.
    - Registo do histórico da conversa.
- Registro e resolução de desacordos.
    - Registo da decisão final sobre um desacordo.
    - Manutenção do histórico de alterações.
    - Possibilidade de revisões futuras.

### **3. Gestão de Perspetivas Anotadoras - 5 casos de uso**
- Permitir que anotadores registrem a sua perspetiva.
    - Campo adicional na interface para adicionar contexto.
    - Opção de escolher categorias de perspetivas (ex: cultural, técnica, subjetiva).
- Associar anotações a perspetivas específicas.
    - Ligação automática entre anotação e perspetiva.
    - Listagem de anotações com indicação da perspetiva.
- Filtragem e visualização baseada em perspetivas.
    - Filtro por tipo de perspetiva na interface.
    - Comparação de anotações por perspetiva.
    - Gráficos demonstrativos de tendências.
- Análise estatística das tendências nas anotações.
    - Cálculo da frequência de cada perspetiva.
    - Comparação entre anotadores.
    - Exportação de estatísticas.
- Geração de relatórios sobre as influências das perspetivas.
    - Relatório detalhado com impacto das perspetivas.
    - Identificação de padrões de anotação.

### **4. Resolução Colaborativa de Desacordos - 3 casos de uso adicionais**
- Criar uma discussão sobre uma discrepância.
    - Criar um novo tópico de discussão.
    - Convidar outros anotadores para opinar.
- Votação para resolução de um desacordo.
    - Cada anotador pode votar na melhor solução.
    - Votação com tempo limite.
- Manutenção do histórico de decisões e discussões.
    - Registo detalhado do que foi decidido.
    - Possibilidade de revisões futuras das decisões.

### **5. Relatórios de Desacordo e Perspetiva - 2 casos de uso adicionais**
- Geração de relatórios sobre desacordos.
    - Criar gráficos sobre quantidade e tipos de desacordos.
    - Exibição do histórico de alterações.
- Exportação de dados para análise externa (PDF, CSV).
    - Exportação para CSV e PDF.
    - Seleção de filtros antes da exportação.

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-repo/doccano-extensao.git
cd doccano-extensao

(por acabar)

```
🔗 Aceder em: [http://localhost:8000](http://localhost:8000)

---

## Contribuição
Se quiser contribuir, abra um **pull request** ou relate problemas na secção de **issues** do repositório.
Agradecemos por todo o feedback dado.

---

## Licença
Este projeto segue a mesma **licença** do [Doccano](https://github.com/doccano/doccano).
