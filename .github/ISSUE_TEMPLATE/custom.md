---
name: 📝 Issue genérica
about: Use este template para reportar um problema, dúvida ou sugestão que não se enquadre em outros templates.
title: ''
labels: ''
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## Descrição
        Por favor, descreva seu problema, dúvida ou sugestão de forma clara.

  - type: textarea
    id: description
    attributes:
      label: Descrição detalhada
      placeholder: Explique o que está acontecendo, qual comportamento esperado, etc.
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Passos para reproduzir (se aplicável)
      placeholder: Liste os passos para reproduzir o problema.

  - type: textarea
    id: context
    attributes:
      label: Contexto adicional
      placeholder: Informação adicional que possa ajudar na análise.

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: Verifiquei se há outros templates mais adequados.
        - label: Descrevi o problema de forma clara.
      required: true
---