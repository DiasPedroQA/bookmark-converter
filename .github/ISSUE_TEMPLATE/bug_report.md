---
name: 🐞 Reporte de Bug
about: Informe um problema ou comportamento inesperado no HTMLReader para nos ajudar a melhorar
title: "[Bug] "
labels: [bug]
assignees: []

body:

- type: markdown
    attributes:
      value: |
        ## 📄 Descrição do Problema
        Por favor, descreva de forma clara e concisa qual é o problema encontrado.

- type: textarea
    id: description
    attributes:
      label: Descrição do bug
      placeholder: Explique detalhadamente o problema que você encontrou...
      required: true

- type: markdown
    attributes:
      value: |
        ## 🔁 Passos para Reproduzir
        Liste os passos exatos para reproduzir o problema:

- type: textarea
    id: steps
    attributes:
      label: Passos para reproduzir
      placeholder: |
        1. Vá para '...'
        2. Clique em '...'
        3. Role para '...'
        4. Veja o erro acontecer
      required: true

- type: markdown
    attributes:
      value: |
        ## ✅ Comportamento Esperado
        O que você esperava que acontecesse?

- type: textarea
    id: expected_behavior
    attributes:
      label: Comportamento esperado
      placeholder: Descreva qual seria o comportamento correto esperado
      required: true

- type: markdown
    attributes:
      value: |
        ## 🧪 Ambiente de Execução

- type: checkboxes
    id: operating_system
    attributes:
      label: Sistema Operacional
      description: Selecione todos os que se aplicam
      options:
        - label: Windows
          value: windows
        - label: macOS
          value: macos
        - label: Linux
          value: linux

- type: input
    id: python_version
    attributes:
      label: Versão do Python
      description: Exemplo: 3.12.0
      placeholder: Ex: 3.12.0

- type: dropdown
    id: interface_used
    attributes:
      label: Interface utilizada
      options:
        - GUI (Tkinter)
        - CLI
        - API (FastAPI)

- type: markdown
    attributes:
      value: |
        ## 📱 Informações sobre Dispositivo Móvel (se aplicável)

- type: input
    id: device
    attributes:
      label: Dispositivo
      description: Exemplo: iPhone 13

- type: input
    id: os_mobile
    attributes:
      label: Sistema Operacional do Dispositivo Móvel
      description: Exemplo: iOS 17

- type: input
    id: browser_mobile
    attributes:
      label: Navegador Móvel
      description: Exemplo: Safari

- type: input
    id: browser_version_mobile
    attributes:
      label: Versão do Navegador Móvel
      description: Exemplo: 17.3.1

- type: textarea
    id: additional_context
    attributes:
      label: Contexto Adicional
      description: Logs, mensagens de erro, links úteis ou qualquer outra informação relevante

- type: checkboxes
    id: checklist
    attributes:
      label: Checklist antes de enviar
      options:
        - label: Verifiquei se esse bug já foi reportado antes
        - label: Estou usando a versão mais recente disponível do projeto
        - label: Estou disposto(a) a ajudar com a correção (se possível)
      required: true
---