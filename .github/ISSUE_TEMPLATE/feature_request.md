---
name: 💡 Feature Request
about: Sugira uma nova funcionalidade ou melhoria para o HTMLReader
title: "[Feature] "
labels: [enhancement]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## 📝 Descrição da funcionalidade
        Por favor, descreva a nova funcionalidade ou melhoria que você gostaria de sugerir.

  - type: textarea
    id: feature_description
    attributes:
      label: Descrição da funcionalidade
      placeholder: Explique sua ideia de forma clara e detalhada...
      required: true

  - type: markdown
    attributes:
      value: |
        ## 🎯 Objetivo
        Qual problema essa funcionalidade resolve ou qual benefício ela trará?

  - type: textarea
    id: feature_goal
    attributes:
      label: Objetivo da funcionalidade
      placeholder: Descreva o objetivo principal dessa funcionalidade.
      required: true

  - type: markdown
    attributes:
      value: |
        ## 💡 Alternativas já consideradas
        Você já pensou em outras soluções ou alternativas? Quais?

  - type: textarea
    id: alternatives
    attributes:
      label: Alternativas consideradas
      placeholder: Liste as alternativas que você já avaliou.

  - type: markdown
    attributes:
      value: |
        ## 📚 Contexto adicional
        Alguma informação extra, links ou exemplos que possam ajudar a entender a solicitação.

  - type: textarea
    id: additional_context
    attributes:
      label: Contexto adicional
      placeholder: Informação extra, links, imagens, etc.

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist antes de enviar
      options:
        - label: Procurei se essa funcionalidade já foi solicitada.
        - label: Descrevi o problema ou a melhoria de forma clara.
        - label: Estou disposto(a) a ajudar no desenvolvimento (se possível).
      required: true
---
