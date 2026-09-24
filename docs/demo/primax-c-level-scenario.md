# Enterprise C-Level FAST DEMO — Executive Scenario

> All project and contract data in this scenario is synthetic and exists only to demonstrate the orchestration pattern.

## Opening experience

**¿En qué te ayudo?**

The user does not select an agent. The Enterprise Meta-Orchestrator discovers capabilities and coordinates domains.

## Demo sequence

1. **Portfolio only**
   - User: `¿Cuál es el avance del proyecto PRJ-001?`
   - Expected route: Portfolio.
   - Expected evidence: PRJ-001 demo record.

2. **Contextual follow-up**
   - User: `¿Cuál es su próximo hito y qué dependencias tiene?`
   - Context: `project_id=PRJ-001`.
   - Expected route: Portfolio.

3. **Legal**
   - User: `¿Qué riesgo contractual puede afectar al proyecto PRJ-001?`
   - Expected route: Legal + Portfolio when the wording contains both domains.
   - Legal evidence: DEMO-LEGAL-001.

4. **Executive WOW moment**
   - User: `¿Cuál es el avance del proyecto PRJ-001 y qué riesgos tiene su contrato?`
   - Expected route: Legal + Portfolio.
   - Expected output: one response, domain provenance, evidence from both domains and human-review boundary for legal findings.

5. **Safe boundary**
   - User asks about an unsupported enterprise domain.
   - Expected: explicit unsupported/abstention; no invented capability.

## Visible orchestration states

```text
Comprendiendo tu solicitud...
Identificando capacidades...
Consultando Gestión de Portafolio...
Consultando Legal...
Consolidando evidencia...
Preparando respuesta ejecutiva...
```

## C-Level message

> Una sola conversación puede coordinar capacidades empresariales especializadas sin obligar al usuario a conocer qué agente debe utilizar.
