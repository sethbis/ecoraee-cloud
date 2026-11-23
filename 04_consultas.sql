-- ============================================================================
-- PROYECTO INTEGRADOR - QUINTO SEMESTRE 2026
-- ASIGNATURA: SISTEMAS DE GESTIÓN DE BASES DE DATOS (05-SIN-A)
-- UNIVERSIDAD INTERNACIONAL DEL ECUADOR (UIDE) / ARIZONA STATE UNIVERSITY
-- INTEGRANTES: Daniel Fernando Pazmiño Mera, Matías Nicolás Herrera Cueva, Ihair Geordano Llamuca López
-- DOCENTE: Ing. María del Carmen Salazar Torres, Mgtr.
-- MOTOR: MICROSOFT SQL SERVER (T-SQL)
-- ARCHIVO: 04_consultas.sql
-- DESCRIPCIÓN: CONSULTAS ANALÍTICAS Y TRANSACCIONALES PARA EL ECOSISTEMA ECORAEE.
--              CUMPLE CON EL USO DE INNER/LEFT JOIN, AGRUPACIONES GROUP BY Y
--              SUBCONSULTAS ESCALARES Y CORRELACIONADAS:
--              a) Historial cronológico de estados de un dispositivo.
--              b) Inventario consolidado por centro de acopio y estado.
--              c) Resumen de dispositivos por categoría y clasificación técnica.
--              d) Indicador de porcentaje de dispositivos con trazabilidad cerrada.
--              e) Dispositivos recibidos pendientes de evaluación técnica.
-- ============================================================================

USE BD_ECORAEE_CLOUD;
GO

SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO

SET NOCOUNT ON;
GO

PRINT '==============================================================================';
PRINT 'INICIO DEL SCRIPT 04_consultas.sql: CONSULTAS AVANZADAS DEL ECOSISTEMA';
PRINT '==============================================================================';
GO

-- ============================================================================
-- CONSULTA A: HISTORIAL DE ESTADOS DE UN DISPOSITIVO (TRAZABILIDAD COMPLETA)
-- ============================================================================
-- Requerimiento: Mostrar cronológicamente la trazabilidad ininterrumpida de un equipo.
-- Filtro: Se evalúa el Dispositivo 1 (Laptop Dell del Ciclo 1 - Reutilizable).
-- Características técnicas: 
--   - Múltiples INNER JOIN para enriquecer la entidad débil HISTORIAL_ESTADO.
--   - Cruce con ESTADO_DISPOSITIVO, USUARIO, EMPLEADO y PERSONA_NATURAL.
--   - Ordenamiento cronológico ascendente por numero_secuencia (clave parcial).
-- ============================================================================

PRINT '>>> Ejecutando Consulta A: Historial de estados del Dispositivo 1...';
GO

SELECT 
    d.id_dispositivo,
    d.codigo_qr,
    COALESCE(d.numero_serie, 'SIN_SERIE_REGISTRADA') AS numero_serie,
    cat.nombre AS categoria,
    m.nombre AS modelo,
    h.numero_secuencia AS secuencia,
    e.codigo AS codigo_estado,
    e.nombre AS estado_operativo,
    h.fecha_inicio,
    h.fecha_fin,
    CONCAT(pn.nombres, ' ', pn.apellidos) AS usuario_responsable,
    rs.nombre AS rol_institucional,
    h.observacion
FROM HISTORIAL_ESTADO h
INNER JOIN DISPOSITIVO d ON h.id_dispositivo = d.id_dispositivo
INNER JOIN MODELO_DISPOSITIVO m ON d.id_modelo = m.id_modelo
INNER JOIN CATEGORIA_DISPOSITIVO cat ON m.id_categoria = cat.id_categoria
INNER JOIN ESTADO_DISPOSITIVO e ON h.id_estado = e.id_estado
INNER JOIN USUARIO u ON h.id_usuario = u.id_usuario
INNER JOIN EMPLEADO emp ON u.id_empleado = emp.id_empleado
INNER JOIN PERSONA_NATURAL pn ON emp.id_persona = pn.id_persona
INNER JOIN ROL_SISTEMA rs ON u.id_rol_sistema = rs.id_rol_sistema
WHERE d.id_dispositivo = 1
ORDER BY h.numero_secuencia ASC;
GO


-- ============================================================================
-- CONSULTA B: INVENTARIO POR CENTRO Y ESTADO (DISPONIBILIDAD EN BODEGAS)
-- ============================================================================
-- Requerimiento: Totalizar la cantidad de dispositivos y el peso acumulado (kg) 
--                presentes físicamente en cada centro de acopio o laboratorio,
--                desglosados por el estado actual en el que se encuentran.
-- Características técnicas:
--   - INNER JOIN entre CENTRO_ACOPIO, INVENTARIO, DISPOSITIVO y ESTADO_DISPOSITIVO.
--   - Subconsulta correlacionada para extraer el último estado registrado en la entidad débil.
--   - Agrupación GROUP BY multivariable y funciones de agregación COUNT() y SUM().
-- ============================================================================

PRINT '>>> Ejecutando Consulta B: Inventario actual por centro y estado operativo...';
GO

SELECT 
    c.id_centro,
    c.codigo_centro,
    c.nombre AS centro_acopio,
    tc.nombre AS tipo_instalacion,
    e.nombre AS estado_actual,
    COUNT(d.id_dispositivo) AS total_dispositivos,
    CAST(SUM(d.peso_kg) AS DECIMAL(10,2)) AS peso_total_kg,
    CAST(AVG(d.peso_kg) AS DECIMAL(8,2)) AS peso_promedio_kg
FROM INVENTARIO inv
INNER JOIN CENTRO_ACOPIO c ON inv.id_centro = c.id_centro
INNER JOIN TIPO_CENTRO tc ON c.id_tipo_centro = tc.id_tipo_centro
INNER JOIN DISPOSITIVO d ON inv.id_dispositivo = d.id_dispositivo
-- Subconsulta correlacionada para determinar el estado más reciente de cada equipo
INNER JOIN HISTORIAL_ESTADO h ON d.id_dispositivo = h.id_dispositivo
    AND h.numero_secuencia = (
        SELECT MAX(h_sub.numero_secuencia)
        FROM HISTORIAL_ESTADO h_sub
        WHERE h_sub.id_dispositivo = d.id_dispositivo
    )
INNER JOIN ESTADO_DISPOSITIVO e ON h.id_estado = e.id_estado
GROUP BY 
    c.id_centro,
    c.codigo_centro,
    c.nombre,
    tc.nombre,
    e.nombre
ORDER BY c.nombre ASC, e.nombre ASC;
GO


-- ============================================================================
-- CONSULTA C: DISPOSITIVOS POR CATEGORÍA Y CLASIFICACIÓN TÉCNICA
-- ============================================================================
-- Requerimiento: Evaluar el rendimiento del triage técnico, agrupando los RAEE
--                evaluados según su categoría funcional y su clasificación de destino
--                (Reutilizable, Reparable, Reciclable, No recuperable).
-- Características técnicas:
--   - Cruce de EVALUACION_TECNICA con DISPOSITIVO, MODELO_DISPOSITIVO,
--     CATEGORIA_DISPOSITIVO y CLASIFICACION_TECNICA.
--   - GROUP BY con agregaciones cuantitativas y métricas de peso.
-- ============================================================================

PRINT '>>> Ejecutando Consulta C: Dispositivos por categoría y clasificación técnica...';
GO

SELECT 
    cat.codigo AS codigo_categoria,
    cat.nombre AS categoria_raee,
    cl.codigo AS codigo_clasificacion,
    cl.nombre AS dictamen_tecnico,
    CASE 
        WHEN cl.permite_donacion = 1 THEN 'APTO_DONACION_SOCIAL'
        ELSE 'DESTINO_INDUSTRIAL_DISPOSICION'
    END AS viabilidad_social,
    COUNT(d.id_dispositivo) AS cantidad_dispositivos,
    CAST(SUM(d.peso_kg) AS DECIMAL(10,2)) AS peso_total_kg,
    CAST(AVG(d.peso_kg) AS DECIMAL(8,2)) AS peso_promedio_kg
FROM EVALUACION_TECNICA ev
INNER JOIN DISPOSITIVO d ON ev.id_dispositivo = d.id_dispositivo
INNER JOIN MODELO_DISPOSITIVO m ON d.id_modelo = m.id_modelo
INNER JOIN CATEGORIA_DISPOSITIVO cat ON m.id_categoria = cat.id_categoria
INNER JOIN CLASIFICACION_TECNICA cl ON ev.id_clasificacion = cl.id_clasificacion
GROUP BY 
    cat.codigo,
    cat.nombre,
    cl.codigo,
    cl.nombre,
    cl.permite_donacion
ORDER BY cat.nombre ASC, cl.nombre ASC;
GO


-- ============================================================================
-- CONSULTA D: PORCENTAJE DE DISPOSITIVOS CON TRAZABILIDAD CERRADA (KPI CIRCULAR)
-- ============================================================================
-- Requerimiento: Obtener la tasa de éxito de cierre de ciclo de vida del ecosistema.
--                Determina qué porcentaje de todos los equipos registrados ya poseen
--                su trazabilidad cerrada formalmente en la tabla DESTINO_FINAL (RN-08).
-- Características técnicas:
--   - LEFT JOIN entre DISPOSITIVO y DESTINO_FINAL.
--   - Subconsulta escalar integrada: (SELECT COUNT(*) FROM DISPOSITIVO).
--   - Agregación condicional con SUM(CASE WHEN ...) y cálculo porcentual con control de división por cero.
-- ============================================================================

PRINT '>>> Ejecutando Consulta D: Indicador porcentual de trazabilidad cerrada...';
GO

SELECT 
    (SELECT COUNT(*) FROM DISPOSITIVO) AS total_dispositivos_captados,
    SUM(CASE WHEN df.id_destino_final IS NOT NULL THEN 1 ELSE 0 END) AS dispositivos_trazabilidad_cerrada,
    SUM(CASE WHEN df.id_destino_final IS NULL THEN 1 ELSE 0 END) AS dispositivos_en_proceso_activo,
    CAST(
        (CAST(SUM(CASE WHEN df.id_destino_final IS NOT NULL THEN 1 ELSE 0 END) AS DECIMAL(10,2)) * 100.0) 
        / NULLIF((SELECT COUNT(*) FROM DISPOSITIVO), 0)
        AS DECIMAL(5,2)
    ) AS tasa_cierre_trazabilidad_pct,
    CAST(
        (CAST(SUM(CASE WHEN df.id_destino_final IS NULL THEN 1 ELSE 0 END) AS DECIMAL(10,2)) * 100.0) 
        / NULLIF((SELECT COUNT(*) FROM DISPOSITIVO), 0)
        AS DECIMAL(5,2)
    ) AS tasa_en_operacion_pct
FROM DISPOSITIVO d
LEFT JOIN DESTINO_FINAL df ON d.id_dispositivo = df.id_dispositivo;
GO


-- ============================================================================
-- CONSULTA E: DISPOSITIVOS RECIBIDOS QUE AÚN NO TIENEN EVALUACIÓN TÉCNICA
-- ============================================================================
-- Requerimiento: Identificar cuellos de botella de diagnóstico. Lista los equipos
--                que ya se encuentran físicamente en bodega (INVENTARIO) pero que
--                aún carecen de un diagnóstico formal en EVALUACION_TECNICA.
-- Características técnicas:
--   - INNER JOIN entre DISPOSITIVO, MODELO_DISPOSITIVO, CATEGORIA_DISPOSITIVO,
--     INVENTARIO, CENTRO_ACOPIO y UBICACION.
--   - Cláusula WHERE con SUBCONSULTA NOT IN para filtrar exclusiones de conjuntos.
--   - Cálculo de antigüedad en días mediante DATEDIFF() para priorización de triage.
-- ============================================================================

PRINT '>>> Ejecutando Consulta E: Dispositivos en bodega pendientes de diagnóstico...';
GO

SELECT 
    d.id_dispositivo,
    d.codigo_qr,
    COALESCE(d.numero_serie, 'SIN_SERIE_REGISTRADA') AS numero_serie,
    cat.nombre AS categoria,
    m.nombre AS modelo,
    c.nombre AS centro_acopio_actual,
    COALESCE(ub.codigo_ubicacion, 'AREA_RECEPCION_PRELIMINAR') AS estante_bodega,
    d.peso_kg,
    CONVERT(VARCHAR(19), d.fecha_registro, 120) AS fecha_ingreso,
    DATEDIFF(DAY, d.fecha_registro, SYSDATETIME()) AS dias_espera_diagnostico
FROM DISPOSITIVO d
INNER JOIN MODELO_DISPOSITIVO m ON d.id_modelo = m.id_modelo
INNER JOIN CATEGORIA_DISPOSITIVO cat ON m.id_categoria = cat.id_categoria
INNER JOIN INVENTARIO inv ON d.id_dispositivo = inv.id_dispositivo
INNER JOIN CENTRO_ACOPIO c ON inv.id_centro = c.id_centro
LEFT JOIN UBICACION ub ON inv.id_ubicacion = ub.id_ubicacion
WHERE d.id_dispositivo NOT IN (
    -- Subconsulta: Dispositivos que ya cuentan con diagnóstico técnico registrado
    SELECT DISTINCT ev.id_dispositivo 
    FROM EVALUACION_TECNICA ev
)
ORDER BY d.fecha_registro ASC, d.id_dispositivo ASC;
GO

PRINT '==============================================================================';
PRINT 'FIN DEL SCRIPT 04_consultas.sql: TODAS LAS CONSULTAS EJECUTADAS CON ÉXITO.';
PRINT '==============================================================================';
GO
