# Este diccionario contiene recomendaciones genéricas para cada KPA
# Las uso cuando detecto que una KPA tiene problemas (respuestas "Parcial" o "No")
# Son consejos prácticos que ayudarán a mejorar cada área de proceso

RECOMENDACIONES_BASE = {
    # Recomendaciones para mejorar la Gestión de requisitos
    # Me enfoco en formalizar, documentar y mantener trazabilidad
    "Gestión de requisitos": [
        "Formalizar la documentación completa de requisitos (funcionales y no funcionales).",
        "Implementar una matriz de trazabilidad entre requisitos y entregables/casos de prueba.",
        "Establecer revisiones periódicas con stakeholders para validar requisitos."
    ],
    
    # Recomendaciones para una mejor Planificación de proyectos
    # Incluyo la importancia de un plan formal, análisis de riesgos y actualizaciones continuas
    "Planificación de proyectos": [
        "Elaborar un plan de proyecto formal: objetivos, alcance, cronograma y recursos.",
        "Incluir análisis de riesgos y planes de mitigación en la planificación.",
        "Revisar y actualizar el plan periódicamente con el equipo."
    ],
    
    # Recomendaciones para mejorar el Seguimiento y control
    # Sugiero establecer métricas, reuniones regulares y documentación de desviaciones
    "Seguimiento y control de proyectos": [
        "Definir métricas de avance y rendimiento (por ejemplo: porcentaje de tareas completadas).",
        "Establecer reuniones de seguimiento semanales y registrar actas.",
        "Documentar desviaciones y acciones correctivas."
    ],
    
    # Recomendaciones para la Gestión de configuración
    # Propongo usar Git, documentar versiones y establecer políticas claras
    "Gestión de configuración": [
        "Adoptar control de versiones (por ejemplo Git) con una política de ramas.",
        "Documentar cambios, versiones y releases del software.",
        "Establecer una política de gestión de configuración y seguimiento de artefactos."
    ],
    
    # Recomendaciones para el Aseguramiento de calidad
    # Aconsejo definir criterios claros, implementar pruebas y registrar defectos
    "Aseguramiento de calidad": [
        "Definir criterios de calidad para cada entrega y revisar su cumplimiento.",
        "Implementar pruebas unitarias, de integración y registrar resultados.",
        "Establecer un proceso para registrar y analizar defectos y acciones correctivas."
    ]
}