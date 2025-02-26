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
- Editar utilizador.
- Remover utilizador.
- Consultar utilizadores.
- Atribuir permissões e papéis.
- Alterar permissões de utilizadores.
- Reset de senha/autenticação.
- Listagem filtrada de utilizadores.

### **2. Gestão de Desacordos entre Anotadores - 5 casos de uso**
- Identificação automática de discrepâncias entre anotações.
- Sinalização visual de desacordos.
- Apresentação lado a lado de anotações divergentes.
- Permite discussão sobre as diferenças diretamente na interface.
- Registro e resolução de desacordos.

### **3. Gestão de Perspetivas Anotadoras - 5 casos de uso**
- Permitir que anotadores registrem a sua perspetiva.
- Associar anotações a perspetivas específicas.
- Filtragem e visualização baseada em perspetivas.
- Análise estatística das tendências nas anotações.
- Geração de relatórios sobre as influências das perspetivas.

### **4. Resolução Colaborativa de Desacordos - 3 casos de uso adicionais**
- Criar uma discussão sobre uma discrepância.
- Votação para resolução de um desacordo.
- Manutenção do histórico de decisões e discussões.

### **5. Relatórios de Desacordo e Perspetiva - 2 casos de uso adicionais**
- Geração de relatórios sobre desacordos.
- Exportação de dados para análise externa (PDF, CSV).

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