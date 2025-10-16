# Este diccionario almacena las 5 Áreas Clave de Proceso (KPAs) del Nivel 2 de CMMI
# Cada KPA tiene asociada una lista de 5 preguntas que evalúan su nivel de implementación
# Utilizo este diccionario como base de datos de preguntas para la evaluación

KPAS = {
    # Primera KPA: Me enfoco en cómo se gestionan los requisitos del proyecto
    # Evalúo documentación, trazabilidad, control de cambios y comunicación con stakeholders
    "Gestión de requisitos": [
        "¿Se documentan los requisitos funcionales y no funcionales?",
        "¿Existe trazabilidad entre requisitos y entregables?",
        "¿Se gestiona formalmente el cambio de requisitos?",
        "¿Se revisan los requisitos con los stakeholders?",
        "¿Se almacenan los requisitos en un repositorio accesible?"
    ],
    
    # Segunda KPA: Verifico si existe una planificación formal y realista del proyecto
    # Incluye estimación de recursos, identificación de riesgos y asignación de responsabilidades
    "Planificación de proyectos": [
        "¿Existe un plan de proyecto formalmente definido?",
        "¿Se estiman recursos y plazos de forma realista?",
        "¿Se identifican riesgos y planes de mitigación?",
        "¿Se asignan responsabilidades claramente?",
        "¿Se actualiza el plan tras cambios relevantes?"
    ],
    
    # Tercera KPA: Evalúo el seguimiento continuo del proyecto mediante métricas
    # Compruebo si se documentan problemas, desviaciones y se reporta el estado
    "Seguimiento y control de proyectos": [
        "¿Se mide el avance regularmente (métricas)?",
        "¿Se documentan desviaciones y acciones correctivas?",
        "¿Se realizan reuniones de seguimiento periódicas?",
        "¿Se gestionan problemas y decisiones formalmente?",
        "¿Se hace un reporte de estado a stakeholders?"
    ],
    
    # Cuarta KPA: Analizo el control de versiones y la gestión de cambios
    # Verifico si hay políticas establecidas para branching, merging y versionado
    "Gestión de configuración": [
        "¿Se usa control de versiones para el código?",
        "¿Se documentan releases y versiones del software?",
        "¿Existe una política de branching/merging establecida?",
        "¿Se registran cambios y motivos de cambio?",
        "¿Se mantienen artefactos (builds, entregables) controlados?"
    ],
    
    # Quinta KPA: Evalúo los procesos de aseguramiento de calidad del proyecto
    # Incluye criterios de calidad, pruebas, registro de defectos y automatización
    "Aseguramiento de calidad": [
        "¿Se definen criterios de calidad para entregas?",
        "¿Se realizan pruebas unitarias e integración sistemáticas?",
        "¿Se registran y analizan defectos?",
        "¿Se realizan revisiones y auditorías de calidad?",
        "¿Se automatizan pruebas y/o procesos de CI?"
    ]
}