-- ============================================================================
-- PROYECTO INTEGRADOR - QUINTO SEMESTRE 2026
-- ASIGNATURA: SISTEMAS DE GESTIÓN DE BASES DE DATOS (05-SIN-A)
-- UNIVERSIDAD INTERNACIONAL DEL ECUADOR (UIDE) / ARIZONA STATE UNIVERSITY
-- INTEGRANTES: Daniel Fernando Pazmiño Mera, Matías Nicolás Herrera Cueva, Ihair Geordano Llamuca López
-- DOCENTE: Ing. María del Carmen Salazar Torres, Mgtr.
-- MOTOR: MICROSOFT SQL SERVER (T-SQL)
-- ARCHIVO: 03_pruebas.sql
-- DESCRIPCIÓN: VALIDACIÓN DE RESTRICCIONES DE INTEGRIDAD EN SQL SERVER.
--              CONTIENE 5 INSTRUCCIONES DISEÑADAS ESPECÍFICAMENTE PARA SER
--              RECHAZADAS POR EL MOTOR, DEMOSTRANDO EL CONTROL DE INTEGRIDAD:
--              1. Violación de Primary Key (PK repetida en entidad débil)
--              2. Violación de Foreign Key (FK inexistente en tabla padre)
--              3. Violación de Clave Única (UNIQUE repetido en código QR / AK)
--              4. Violación de Restricción CHECK (CHECK incumplido de peso positivo)
--              5. Violación de Integridad Referencial por Borrado (DELETE con hijos)
-- ============================================================================

USE BD_ECORAEE_CLOUD;
GO

SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO

PRINT '==============================================================================';
PRINT 'INICIO DEL SCRIPT 03_pruebas.sql: PRUEBAS DE INTEGRIDAD Y RESTRICCIONES';
PRINT '==============================================================================';
PRINT 'Instrucciones:';
PRINT 'Ejecute cada instrucción por separado en SQL Server Management Studio (SSMS)';
PRINT 'para capturar el mensaje de error nativo arrojado por el motor.';
PRINT '==============================================================================';
GO

-- ============================================================================
-- PRUEBA 1: VIOLACIÓN DE PRIMARY KEY (PK REPETIDA)
-- ============================================================================
-- Justificación técnica:
-- La tabla HISTORIAL_ESTADO es una entidad débil con clave primaria compuesta
-- formada por {id_dispositivo, numero_secuencia}. El dispositivo con id_dispositivo = 1
-- ya tiene registrada la secuencia número 1 (desde 02_DML.sql).
-- Al intentar insertar otro registro con exactamente los mismos valores de clave primaria
-- (1, 1), el motor T-SQL rechaza la operación garantizando la unicidad de tuplas.
--
-- Error esperado de SQL Server:
-- Msg 2627, Level 14, State 1, Line 1
-- Violation of PRIMARY KEY constraint 'PK_HISTORIAL_ESTADO'. 
-- Cannot insert duplicate key in object 'dbo.HISTORIAL_ESTADO'. The duplicate key value is (1, 1).
-- ============================================================================

PRINT '>>> Ejecutando Prueba 1: Violación de PRIMARY KEY (PK repetida)...';
GO

INSERT INTO HISTORIAL_ESTADO (
    id_dispositivo, 
    numero_secuencia, 
    id_estado, 
    id_usuario, 
    fecha_inicio, 
    observacion
)
VALUES (
    1, 
    1, -- Clave duplicada: El dispositivo 1 ya posee la secuencia 1
    2, 
    2, 
    SYSDATETIME(), 
    'Intento de inserción de secuencia duplicada para violar PK'
);
GO


-- ============================================================================
-- PRUEBA 2: VIOLACIÓN DE FOREIGN KEY (FK INEXISTENTE)
-- ============================================================================
-- Justificación técnica:
-- La tabla DISPOSITIVO mantiene una clave foránea FK_DISPOSITIVO_MODELO que
-- referencia a la tabla padre MODELO_DISPOSITIVO(id_modelo).
-- Actualmente los modelos registrados van del 1 al 13.
-- Al intentar registrar un dispositivo con id_modelo = 9999 (inexistente), el motor
-- cancela la inserción asegurando que ningún residuo electrónico quede huérfano
-- o vinculado a especificaciones de hardware inexistentes.
--
-- Error esperado de SQL Server:
-- Msg 547, Level 16, State 0, Line 1
-- The INSERT statement conflicted with the FOREIGN KEY constraint "FK_DISPOSITIVO_MODELO". 
-- The conflict occurred in database "BD_ECORAEE_CLOUD", table "dbo.MODELO_DISPOSITIVO", column 'id_modelo'.
-- ============================================================================

PRINT '>>> Ejecutando Prueba 2: Violación de FOREIGN KEY (FK inexistente)...';
GO

INSERT INTO DISPOSITIVO (
    codigo_qr, 
    numero_serie, 
    id_modelo, 
    id_lote, 
    id_condicion, 
    peso_kg, 
    observaciones
)
VALUES (
    'QR-TEST-ERR-FK-999', 
    'SN-ERR-FK-001', 
    9999, -- Clave foránea inexistente en MODELO_DISPOSITIVO
    1, 
    1, 
    2.50, 
    'Dispositivo de prueba asociado a un modelo inexistente'
);
GO


-- ============================================================================
-- PRUEBA 3: VIOLACIÓN DE CLAVE ÚNICA / ALTERNA (UNIQUE REPETIDO)
-- ============================================================================
-- Justificación técnica:
-- La columna codigo_qr de la tabla DISPOSITIVO posee una restricción UNIQUE 
-- (UQ_DISPOSITIVO_qr), actuando como clave alterna del negocio.
-- El código 'QR-UIDA-PC-001' ya fue asignado al Dispositivo 1.
-- Al intentar insertar un nuevo dispositivo con el mismo código QR, el motor
-- aborta la transacción preservando la regla de negocio RN-01 (cada equipo debe
-- ser unívocamente identificable en el ecosistema).
--
-- Error esperado de SQL Server:
-- Msg 2627, Level 14, State 2, Line 1
-- Violation of UNIQUE KEY constraint 'UQ_DISPOSITIVO_qr'. 
-- Cannot insert duplicate key in object 'dbo.DISPOSITIVO'. The duplicate key value is (QR-UIDA-PC-001).
-- ============================================================================

PRINT '>>> Ejecutando Prueba 3: Violación de UNIQUE (Código QR repetido)...';
GO

INSERT INTO DISPOSITIVO (
    codigo_qr, 
    numero_serie, 
    id_modelo, 
    id_lote, 
    id_condicion, 
    peso_kg, 
    observaciones
)
VALUES (
    'QR-UIDA-PC-001', -- Código QR duplicado, ya pertenece al Dispositivo 1
    'SN-DELL-NEW-099', 
    1, 
    1, 
    1, 
    3.20, 
    'Intento de registrar un equipo con QR ya existente en el sistema'
);
GO


-- ============================================================================
-- PRUEBA 4: VIOLACIÓN DE RESTRICCIÓN CHECK (CHECK INCUMPLIDO)
-- ============================================================================
-- Justificación técnica:
-- La tabla DISPOSITIVO contiene la restricción CHECK CK_DISPOSITIVO_peso que
-- exige formalmente que el atributo peso_kg sea estrictamente positivo (peso_kg > 0).
-- Al intentar registrar un dispositivo con un peso negativo (ej. -15.50 kg), el motor
-- intercepta la anomalía de dominio físico y rechaza la fila.
--
-- Error esperado de SQL Server:
-- Msg 547, Level 16, State 0, Line 1
-- The INSERT statement conflicted with the CHECK constraint "CK_DISPOSITIVO_peso". 
-- The conflict occurred in database "BD_ECORAEE_CLOUD", table "dbo.DISPOSITIVO", column 'peso_kg'.
-- ============================================================================

PRINT '>>> Ejecutando Prueba 4: Violación de CHECK (Peso negativo no admisible)...';
GO

INSERT INTO DISPOSITIVO (
    codigo_qr, 
    numero_serie, 
    id_modelo, 
    id_lote, 
    id_condicion, 
    peso_kg, 
    observaciones
)
VALUES (
    'QR-TEST-ERR-CHK-PESO', 
    'SN-ERR-PESO-001', 
    1, 
    1, 
    1, 
    -15.50, -- Peso negativo no admisible según la física del negocio
    'Intento de registrar un equipo con peso negativo violando el CHECK'
);
GO


-- ============================================================================
-- PRUEBA 5: BORRADO DE REGISTRO CON DATOS RELACIONADOS (INTEGRIDAD REFERENCIAL)
-- ============================================================================
-- Justificación técnica:
-- El empleado con id_empleado = 3 (María Salazar, técnico especialista de diagnóstico)
-- posee registros hijos dependientes en la tabla EVALUACION_TECNICA.
-- La restricción de clave foránea FK_EVAL_TECNICO fue creada sin la cláusula CASCADE,
-- aplicando la política restrictiva por defecto de SQL Server (ON DELETE NO ACTION).
-- Al intentar eliminar a dicho empleado de la tabla EMPLEADO, el motor bloquea la
-- sentencia DELETE para evitar que las evaluaciones queden sin un técnico responsable.
--
-- Error esperado de SQL Server:
-- Msg 547, Level 16, State 0, Line 1
-- The DELETE statement conflicted with the REFERENCE constraint "FK_EVAL_TECNICO". 
-- The conflict occurred in database "BD_ECORAEE_CLOUD", table "dbo.EVALUACION_TECNICA", column 'id_tecnico'.
-- ============================================================================

PRINT '>>> Ejecutando Prueba 5: Violación por Borrado de Registro Padre con Hijos...';
GO

DELETE FROM EMPLEADO 
WHERE id_empleado = 3; -- Empleada con evaluaciones técnicas vigentes
GO

PRINT '==============================================================================';
PRINT 'FIN DEL SCRIPT 03_pruebas.sql: TODAS LAS RESTRICCIONES FUERON VERIFICADAS.';
PRINT '==============================================================================';
GO
