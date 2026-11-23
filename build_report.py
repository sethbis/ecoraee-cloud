# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(r"C:\Users\nicol\.gemini\config\skills\formato-uide\scripts")
from uide_doc_builder import UIDEDocumentBuilder, COLOR_BLACK
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def format_cell(cell, text, bold=False, italic=False, size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = COLOR_BLACK

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{b}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'B0B0B0')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def add_figure_with_caption(doc, img_path, caption_text, width=Inches(6.2)):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10)
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_BLACK

def create_styled_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        format_cell(hdr_cells[i], header_text, bold=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_background(hdr_cells[i], "EAEAEA")
        
    # Data rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(row_data):
            format_cell(row_cells[col_idx], str(cell_value), bold=False, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
            
    # Set column widths if provided
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    # Add space after table
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(6)
    return table

def main():
    builder = UIDEDocumentBuilder()
    
    # Portada oficial institucional UIDE
    builder.setup_cover(
        assignment_title="PROYECTO INTEGRADOR: MODELO RELACIONAL, DICCIONARIO DE DATOS, NORMALIZACIÓN Y SCRIPTS SQL SERVER (FASE 2)",
        students="Daniel Fernando Pazmiño Mera\nMatías Nicolás Herrera Cueva\nIhair Geordano Llamuca López",
        course="SISTEMAS DE GESTIÓN DE BASES DE DATOS (05-SIN-A)",
        professor="ING. MARÍA DEL CARMEN SALAZAR TORRES, MGTR.",
        period="SEPTIEMBRE 2026 – ENERO 2027",
        year="02 de noviembre de 2026",
        lang="es",
        is_group=True
    )
    
    # INTRODUCCIÓN
    builder.add_h1("Introducción y Contexto del Proyecto")
    builder.add_body(
        "El presente informe documenta el paso del Modelo Conceptual y Entidad-Relación Extendido (EER) "
        "hacia una arquitectura de base de datos relacional robusta implementada en Microsoft SQL Server (T-SQL) "
        "para el ecosistema EcoRAEE Cloud. Dicho ecosistema gestiona de manera integral la economía circular de residuos "
        "de aparatos eléctricos y electrónicos (RAEE), garantizando la trazabilidad de punta a punta, el control de inventarios "
        "en centros de acopio, la evaluación técnica especializada, las transferencias logísticas y la confirmación inmutable "
        "del destino final (reutilización/donación, reacondicionamiento en taller, valorización de reciclaje o confinamiento seguro)."
    )
    builder.add_body(
        "La solución se fundamenta en principios estrictos de integridad transaccional, normalización formal hasta Tercera Forma "
        "Normal (3FN) y Forma Normal de Boyce-Codd (BCNF), preservación de cardinalidades mediante claves compuestas en entidades "
        "débiles, control de multiplicidad N:M mediante tablas intermedias y claves secundarias modeladas como restricciones UNIQUE."
    )
    
    # SECCIÓN 1: MODELO RELACIONAL
    builder.add_h1("1. Modelo Relacional")
    builder.add_body(
        "En concordancia con las reglas de transformación formal del modelo EER al modelo relacional, cada entidad fuerte se materializa "
        "en una tabla con su respectiva Clave Primaria (PK); las entidades débiles adoptan una Clave Primaria Compuesta (PK Compuesta) "
        "integrada por la clave foránea de su entidad fuerte más su clave parcial discriminadora; las relaciones de muchos a muchos (N:M) "
        "se transforman en tablas intermedias de cruce; y cada clave secundaria o alterna (AK) del diseño conceptual pasa al motor físico "
        "como una restricción de unicidad estricta (UNIQUE)."
    )
    
    builder.add_h2("1.1. Reglas de Transformación Aplicadas")
    builder.add_bullet(
        "Las entidades débiles HISTORIAL_ESTADO y DETALLE_MOVIMIENTO carecen de existencia autónoma sin sus respectivas entidades fuertes "
        "(DISPOSITIVO y MOVIMIENTO). Por ende, su clave primaria está constituida por la clave foránea del padre sumada a su discriminador secuencial local: "
        "PK_HISTORIAL_ESTADO = {id_dispositivo [FK], numero_secuencia [Parcial]} y "
        "PK_DETALLE_MOVIMIENTO = {id_movimiento [FK], numero_linea [Parcial]}.",
        bold_prefix="Entidades Débiles con PK Compuesta: "
    )
    builder.add_bullet(
        "Las cardinalidades de muchos a muchos identificadas en el negocio se descomponen en tablas intermedias puras: "
        "PERSONA_ROL ({id_persona [FK], id_rol_actor [FK]}), "
        "ESCENARIO_ARISTA ({id_escenario [FK], id_arista [FK]}) y "
        "RESULTADO_ARISTA ({id_resultado [FK], id_arista [FK]}). Cada una posee una PK compuesta que garantiza que una misma relación "
        "no pueda duplicarse.",
        bold_prefix="Relaciones Muchos a Muchos (N:M): "
    )
    builder.add_bullet(
        "Los identificadores alternos del negocio se blindan mediante índices y restricciones UNIQUE para evitar colisiones: "
        "codigo_qr y numero_serie en DISPOSITIVO; correo en PERSONA; numero_identificacion en PERSONA_NATURAL; ruc en PERSONA_JURIDICA; "
        "codigo_empleado y correo_institucional en EMPLEADO; username en USUARIO; codigo_centro en CENTRO_ACOPIO; "
        "codigo_solicitud en SOLICITUD_RECOLECCION; codigo_lote en LOTE; codigo_orden en ORDEN_TRABAJO; y codigo_movimiento en MOVIMIENTO. "
        "Asimismo, se impone UNIQUE sobre id_dispositivo en INVENTARIO (exclusión física atómica: un dispositivo solo puede estar en una bodega a la vez) "
        "y en DESTINO_FINAL (un dispositivo solo puede cerrar su ciclo una única vez).",
        bold_prefix="Claves Secundarias / Alternas (AK) a UNIQUE: "
    )
    builder.add_bullet(
        "La jerarquía de especialización DISPOSITIVO se implementa mediante el mapeo de tabla por subtipo (especialización 1:1), "
        "donde las tablas COMPUTADORA, MONITOR, TABLET, TELEFONO, ROUTER y OTROS_DISPOSITIVOS comparten la misma clave primaria "
        "id_dispositivo [PK/FK] referenciando con eliminación en cascada a la tabla padre.",
        bold_prefix="Jerarquías de Especialización (Subtipos 1:1): "
    )

    builder.add_h2("1.2. Estructura Relacional Formal del Ecosistema")
    
    rel_tables_summary = [
        ("ROL_ACTOR", "id_rol_actor [PK]", "Ninguna", "codigo, nombre", "Catálogo de roles de negocio en economía circular"),
        ("ROL_SISTEMA", "id_rol_sistema [PK]", "Ninguna", "codigo, nombre", "Catálogo de roles de seguridad RBAC"),
        ("TIPO_CENTRO", "id_tipo_centro [PK]", "Ninguna", "codigo, nombre", "Clasificación de instalaciones logísticas"),
        ("CATEGORIA_DISPOSITIVO", "id_categoria [PK]", "Ninguna", "codigo, nombre", "Tipos de residuos electrónicos (RAEE)"),
        ("MARCA", "id_marca [PK]", "Ninguna", "nombre", "Marcas comerciales de hardware"),
        ("MODELO_DISPOSITIVO", "id_modelo [PK]", "id_marca, id_categoria", "(id_marca, nombre)", "Modelos comerciales de equipos"),
        ("CONDICION_DISPOSITIVO", "id_condicion [PK]", "Ninguna", "codigo, nombre", "Condición cosmética/técnica de entrada"),
        ("ESTADO_DISPOSITIVO", "id_estado [PK]", "Ninguna", "codigo, nombre", "Estados terminales y de transición de ciclo"),
        ("CLASIFICACION_TECNICA", "id_clasificacion [PK]", "Ninguna", "codigo, nombre", "Veredictos de diagnóstico (RN-04)"),
        ("PERSONA", "id_persona [PK]", "Ninguna", "correo", "Supertipo de entidades y actores del sistema"),
        ("PERSONA_NATURAL", "id_persona [PK, FK]", "id_persona -> PERSONA", "numero_identificacion", "Subtipo 1:1 de personas naturales"),
        ("PERSONA_JURIDICA", "id_persona [PK, FK]", "id_persona -> PERSONA", "ruc", "Subtipo 1:1 de organizaciones y empresas"),
        ("PERSONA_ROL", "(id_persona, id_rol_actor) [PK]", "id_persona, id_rol_actor", "Ninguna", "Tabla intermedia N:M entre actor y roles"),
        ("EMPLEADO", "id_empleado [PK]", "id_persona", "id_persona, codigo, correo_inst", "Personal técnico y operativo institucional"),
        ("USUARIO", "id_usuario [PK]", "id_empleado, id_rol_sistema", "id_empleado, username", "Cuentas de autenticación y acceso"),
        ("CENTRO_ACOPIO", "id_centro [PK]", "id_tipo_centro", "codigo_centro", "Puntos de acopio, talleres y plantas"),
        ("UBICACION", "id_ubicacion [PK]", "id_centro", "(id_centro, codigo_ubicacion)", "Estanterías y gavetas internas de centros"),
        ("SOLICITUD_RECOLECCION", "id_solicitud [PK]", "id_generador -> PERSONA", "codigo_solicitud", "Peticiones de retiro de residuos"),
        ("LOTE", "id_lote [PK]", "id_generador, id_solicitud", "codigo_lote", "Agrupación de residuos declarados"),
        ("DISPOSITIVO", "id_dispositivo [PK]", "id_modelo, id_lote, id_condicion", "codigo_qr, numero_serie", "Entidad central del equipo individual"),
        ("COMPUTADORA", "id_dispositivo [PK, FK]", "id_dispositivo -> DISPOSITIVO", "Ninguna", "Subtipo 1:1 para laptops y desktops"),
        ("MONITOR", "id_dispositivo [PK, FK]", "id_dispositivo -> DISPOSITIVO", "Ninguna", "Subtipo 1:1 para pantallas y monitores"),
        ("TABLET", "id_dispositivo [PK, FK]", "id_dispositivo -> DISPOSITIVO", "imei", "Subtipo 1:1 para tabletas digitales"),
        ("TELEFONO", "id_dispositivo [PK, FK]", "id_dispositivo -> DISPOSITIVO", "imei", "Subtipo 1:1 para telefonía inteligente"),
        ("ROUTER", "id_dispositivo [PK, FK]", "id_dispositivo -> DISPOSITIVO", "Ninguna", "Subtipo 1:1 para equipos de telecomunicación"),
        ("HISTORIAL_ESTADO", "(id_dispositivo, numero_secuencia) [PK]", "id_dispositivo, id_estado, id_usuario", "Ninguna", "Entidad débil de auditoría cronológica"),
        ("INVENTARIO", "id_inventario [PK]", "id_centro, id_ubicacion, id_dispositivo", "id_dispositivo", "Ubicación física actual con exclusión atómica"),
        ("EVALUACION_TECNICA", "id_evaluacion [PK]", "id_dispositivo, id_tecnico, id_clasificacion", "Ninguna", "Dictamen técnico pericial (RN-02)"),
        ("ORDEN_TRABAJO", "id_orden [PK]", "id_dispositivo, id_responsable, id_tipo, id_estado", "codigo_orden", "Órdenes de mantenimiento y reparación"),
        ("MOVIMIENTO", "id_movimiento [PK]", "id_centro_origen, id_centro_destino, id_responsable, id_estado", "codigo_movimiento", "Cabecera de flete y traslado entre nodos"),
        ("DETALLE_MOVIMIENTO", "(id_movimiento, numero_linea) [PK]", "id_movimiento, id_dispositivo", "(id_movimiento, id_dispositivo)", "Entidad débil: línea de carga de flete"),
        ("DESTINO_FINAL", "id_destino_final [PK]", "id_dispositivo, id_tipo_destino, id_receptor", "id_dispositivo", "Cierre inmutable de trazabilidad (RN-08)"),
        ("EVIDENCIA", "id_evidencia [PK]", "id_tipo_evidencia, id_dispositivo, id_movimiento, id_usuario", "Ninguna", "Metadatos de soporte fotográfico en S3"),
        ("NODO_RED", "id_nodo [PK]", "id_centro", "codigo_nodo, id_centro", "Vértices del grafo G=(V,E) de flujo máximo"),
        ("ARISTA_RED", "id_arista [PK]", "id_nodo_origen, id_nodo_destino", "(id_nodo_origen, id_nodo_destino)", "Conexiones con capacidad del grafo"),
    ]
    
    headers_rel = ["Tabla", "Clave Primaria (PK)", "Claves Foráneas (FK)", "Claves Alternas (UNIQUE)", "Descripción / Propósito"]
    widths_rel = [Inches(1.5), Inches(1.3), Inches(1.4), Inches(1.3), Inches(1.5)]
    create_styled_table(builder.doc, headers_rel, rel_tables_summary, widths_rel)

    # SECCIÓN 2: DICCIONARIO DE DATOS
    builder.add_h1("2. Diccionario de Datos")
    builder.add_body(
        "A continuación se presenta el diccionario de datos exhaustivo para las tablas fundamentales del ecosistema EcoRAEE Cloud. "
        "Por cada columna se especifica su nombre, tipo de dato físico de SQL Server, nulabilidad, función de clave (PK, FK, AK/UQ), "
        "restricciones de integridad (CHECK, DEFAULT, REFERENCES) y su descripción de negocio."
    )
    
    dict_dispositivo = [
        ("id_dispositivo", "BIGINT IDENTITY(1,1)", "NO", "PK", "PRIMARY KEY CLUSTERED", "Identificador único subrogado del equipo."),
        ("codigo_qr", "VARCHAR(64)", "NO", "AK / UQ", "UNIQUE (UQ_DISPOSITIVO_qr)", "Código QR público para escaneo y trazabilidad rápida."),
        ("numero_serie", "VARCHAR(100)", "SÍ", "AK / UQ", "UNIQUE filtrado (WHERE IS NOT NULL)", "Número de serie de fábrica provisto por el fabricante."),
        ("id_modelo", "INT", "NO", "FK", "REFERENCES MODELO_DISPOSITIVO(id_modelo)", "Referencia obligatoria a marca y categoría del modelo."),
        ("id_lote", "BIGINT", "SÍ", "FK", "REFERENCES LOTE(id_lote)", "Lote de recolección en el cual ingresó el equipo."),
        ("id_condicion", "INT", "NO", "FK", "REFERENCES CONDICION_DISPOSITIVO(id_condicion)", "Condición cosmética y operativa al ingresar a acopio."),
        ("peso_kg", "DECIMAL(8,2)", "NO", "Ninguna", "CHECK (peso_kg > 0)", "Masa física del equipo; alimenta la capacidad de la red."),
        ("fecha_registro", "DATETIME2", "NO", "Ninguna", "DEFAULT (SYSDATETIME())", "Marca temporal inmutable de registro en la plataforma."),
        ("observaciones", "VARCHAR(MAX)", "SÍ", "Ninguna", "Ninguna", "Anotaciones sobre accesorios, cargadores o detalles físicos.")
    ]
    builder.add_h2("2.1. Tabla: DISPOSITIVO (Entidad Fuerte Central)")
    headers_dict = ["Columna", "Tipo de Dato", "Nulos", "Clave", "Restricciones", "Descripción de Negocio"]
    widths_dict = [Inches(1.2), Inches(1.3), Inches(0.5), Inches(0.8), Inches(1.4), Inches(1.8)]
    create_styled_table(builder.doc, headers_dict, dict_dispositivo, widths_dict)

    dict_historial = [
        ("id_dispositivo", "BIGINT", "NO", "PK, FK", "REFERENCES DISPOSITIVO(id_disp) ON DELETE CASCADE", "Clave foránea de la entidad fuerte que compone la PK."),
        ("numero_secuencia", "INT", "NO", "PK (Parcial)", "CHECK (numero_secuencia > 0)", "Discriminador secuencial cronológico (1, 2, 3...)."),
        ("id_estado", "INT", "NO", "FK", "REFERENCES ESTADO_DISPOSITIVO(id_estado)", "Estado alcanzado (Registrado, Recolectado, Evaluado...)."),
        ("id_usuario", "BIGINT", "NO", "FK", "REFERENCES USUARIO(id_usuario)", "Usuario responsable que ejecutó la transición de estado."),
        ("fecha_inicio", "DATETIME2", "NO", "Ninguna", "DEFAULT (SYSDATETIME())", "Momento exacto en que inició la vigencia del estado."),
        ("fecha_fin", "DATETIME2", "SÍ", "Ninguna", "Ninguna", "Momento en que concluyó el estado (NULL si está activo)."),
        ("observacion", "VARCHAR(MAX)", "SÍ", "Ninguna", "Ninguna", "Bitácora detallada de eventos ocurridos en esta fase.")
    ]
    builder.add_h2("2.2. Tabla: HISTORIAL_ESTADO (Entidad Débil de Trazabilidad)")
    create_styled_table(builder.doc, headers_dict, dict_historial, widths_dict)

    dict_evaluacion = [
        ("id_evaluacion", "BIGINT IDENTITY(1,1)", "NO", "PK", "PRIMARY KEY CLUSTERED", "Identificador único del dictamen pericial."),
        ("id_dispositivo", "BIGINT", "NO", "FK", "REFERENCES DISPOSITIVO(id_disp) ON DELETE CASCADE", "Dispositivo evaluado por el laboratorio técnico."),
        ("id_tecnico", "BIGINT", "NO", "FK", "REFERENCES EMPLEADO(id_empleado)", "Técnico acreditado que efectuó el diagnóstico (RN-02)."),
        ("id_clasificacion", "INT", "NO", "FK", "REFERENCES CLASIFICACION_TECNICA(id_clasif)", "Dictamen formal: Reutilizable, Reparable, Reciclable..."),
        ("diagnostico_funcional", "VARCHAR(MAX)", "NO", "Ninguna", "Ninguna", "Detalle técnico de operatividad de CPU, RAM, fuente, etc."),
        ("diagnostico_estetico", "VARCHAR(MAX)", "SÍ", "Ninguna", "Ninguna", "Estado de carcasas, bisagras, paneles y serigrafía."),
        ("fecha_evaluacion", "DATETIME2", "NO", "Ninguna", "DEFAULT (SYSDATETIME())", "Fecha y hora en que se emite el informe pericial."),
        ("aprobado_reutilizacion", "BIT", "NO", "Ninguna", "DEFAULT (0)", "Bandera de certificación para canal de donación comunitaria.")
    ]
    builder.add_h2("2.3. Tabla: EVALUACION_TECNICA (Diagnóstico y Clasificación)")
    create_styled_table(builder.doc, headers_dict, dict_evaluacion, widths_dict)

    dict_lote = [
        ("id_lote", "BIGINT IDENTITY(1,1)", "NO", "PK", "PRIMARY KEY CLUSTERED", "Identificador único interno del lote."),
        ("codigo_lote", "VARCHAR(40)", "NO", "AK / UQ", "UNIQUE (UQ_LOTE_codigo)", "Código de identificación visible para rotulación física."),
        ("id_generador", "BIGINT", "NO", "FK", "REFERENCES PERSONA(id_persona)", "Entidad o individuo que dona o da de baja los equipos."),
        ("id_solicitud", "BIGINT", "SÍ", "FK", "REFERENCES SOLICITUD_RECOLECCION(id_sol)", "Solicitud formal que originó el lote (si aplica)."),
        ("fecha_registro", "DATETIME2", "NO", "Ninguna", "DEFAULT (SYSDATETIME())", "Fecha y hora de creación del lote."),
        ("cantidad_declarada", "INT", "NO", "Ninguna", "CHECK (cantidad_declarada > 0)", "Total estimado de unidades manifestadas en origen."),
        ("peso_declarado_kg", "DECIMAL(10,2)", "SÍ", "Ninguna", "CHECK (peso_declarado_kg > 0)", "Peso global preliminar reportado por el donante."),
        ("observaciones", "VARCHAR(MAX)", "SÍ", "Ninguna", "Ninguna", "Comentarios sobre procedencia o estado general del lote.")
    ]
    builder.add_h2("2.4. Tabla: LOTE (Agrupación de Residuos Declarados)")
    create_styled_table(builder.doc, headers_dict, dict_lote, widths_dict)

    dict_movimiento = [
        ("id_movimiento", "BIGINT IDENTITY(1,1)", "NO", "PK", "PRIMARY KEY CLUSTERED", "Identificador secuencial de la orden de flete."),
        ("codigo_movimiento", "VARCHAR(40)", "NO", "AK / UQ", "UNIQUE (UQ_MOV_codigo)", "Guía de remisión o despacho logístico."),
        ("id_centro_origen", "BIGINT", "NO", "FK", "REFERENCES CENTRO_ACOPIO(id_centro)", "Punto de despacho o partida de la carga."),
        ("id_centro_destino", "BIGINT", "NO", "FK", "REFERENCES CENTRO_ACOPIO(id_centro)", "Punto de recepción o llegada de la carga."),
        ("id_responsable", "BIGINT", "NO", "FK", "REFERENCES EMPLEADO(id_empleado)", "Funcionario logístico que autoriza y custodia el traslado."),
        ("id_estado_movimiento", "INT", "NO", "FK", "REFERENCES ESTADO_MOVIMIENTO(id_est)", "Fase logística: Programado, En Tránsito, Entregado."),
        ("fecha_salida", "DATETIME2", "NO", "Ninguna", "DEFAULT (SYSDATETIME())", "Marca temporal de partida del flete."),
        ("fecha_llegada", "DATETIME2", "SÍ", "Ninguna", "Ninguna", "Marca temporal de confirmación física en destino."),
        ("observaciones", "VARCHAR(MAX)", "SÍ", "Ninguna", "CHECK (id_origen <> id_destino)", "Observaciones de ruta y validación de centros distintos.")
    ]
    builder.add_h2("2.5. Tabla: MOVIMIENTO (Cabecera de Transferencia Logística)")
    create_styled_table(builder.doc, headers_dict, dict_movimiento, widths_dict)

    dict_detalle_mov = [
        ("id_movimiento", "BIGINT", "NO", "PK, FK", "REFERENCES MOVIMIENTO(id_mov) ON DELETE CASCADE", "Clave foránea de la orden de traslado fuerte."),
        ("numero_linea", "INT", "NO", "PK (Parcial)", "CHECK (numero_linea > 0)", "Clave parcial discriminadora del ítem cargado (1, 2...)."),
        ("id_dispositivo", "BIGINT", "NO", "FK", "REFERENCES DISPOSITIVO(id_disp)", "Dispositivo transportado físicamente en la unidad."),
        ("peso_kg_transferido", "DECIMAL(8,2)", "NO", "Ninguna", "CHECK (peso_kg_transferido > 0)", "Masa neta verificada en la balanza de pesaje de carga.")
    ]
    builder.add_h2("2.6. Tabla: DETALLE_MOVIMIENTO (Entidad Débil de Carga)")
    create_styled_table(builder.doc, headers_dict, dict_detalle_mov, widths_dict)

    dict_destino_final = [
        ("id_destino_final", "BIGINT IDENTITY(1,1)", "NO", "PK", "PRIMARY KEY CLUSTERED", "Identificador inmutable del acta de cierre."),
        ("id_dispositivo", "BIGINT", "NO", "FK, AK / UQ", "UNIQUE, REFERENCES DISPOSITIVO(id_disp)", "Garantiza que un dispositivo solo tenga un cierre final (RN-08)."),
        ("id_tipo_destino", "INT", "NO", "FK", "REFERENCES TIPO_DESTINO(id_tipo_dest)", "Canal de cierre: Donación, Reciclaje o Confinamiento."),
        ("id_receptor", "BIGINT", "NO", "FK", "REFERENCES PERSONA(id_persona)", "Entidad beneficiaria, escuela, gestor o planta de inertización."),
        ("fecha_confirmacion", "DATE", "NO", "Ninguna", "Ninguna", "Fecha legal en que se firma el traspaso o certificado."),
        ("certificado_numero", "VARCHAR(60)", "SÍ", "Ninguna", "Ninguna", "Número oficial de manifiesto ambiental o acta de entrega."),
        ("observaciones", "VARCHAR(MAX)", "SÍ", "Ninguna", "Ninguna", "Resumen legal del cierre definitivo de trazabilidad.")
    ]
    builder.add_h2("2.7. Tabla: DESTINO_FINAL (Cierre de Ciclo de Vida)")
    create_styled_table(builder.doc, headers_dict, dict_destino_final, widths_dict)

    # SECCIÓN 3: NORMALIZACIÓN
    builder.add_h1("3. Normalización y Dependencias Funcionales")
    builder.add_body(
        "La normalización es el proceso formal mediante el cual se depura el esquema relacional para eliminar anomalías de inserción, "
        "actualización y borrado, garantizando que cada hecho se almacene en un solo lugar y que las relaciones representen fielmente "
        "las restricciones del dominio del negocio. A continuación se detallan las Dependencias Funcionales (DF) y la justificación técnica "
        "de cumplimiento de la Tercera Forma Normal (3FN) y la Forma Normal de Boyce-Codd (BCNF) en las cinco entidades requeridas."
    )

    builder.add_h2("3.1. Normalización de DISPOSITIVO")
    builder.add_body(
        "La entidad DISPOSITIVO almacena los datos intrínsecos de cada equipo captado por el programa. "
        "Sus claves candidatas son id_dispositivo (clave primaria subrogada) y codigo_qr (clave alterna).",
        bold_prefix="Definición de Claves: "
    )
    builder.add_bullet(
        "DF1: id_dispositivo -> {codigo_qr, numero_serie, id_modelo, id_lote, id_condicion, peso_kg, fecha_registro, observaciones}\n"
        "DF2: codigo_qr -> {id_dispositivo, numero_serie, id_modelo, id_lote, id_condicion, peso_kg, fecha_registro, observaciones}\n"
        "DF3: (id_lote) NO determina atributos del dispositivo; representa pertenencia.\n"
        "DF4: (id_modelo) NO determina id_dispositivo, pero sí sus características de hardware.",
        bold_prefix="Dependencias Funcionales (DFs): "
    )
    builder.add_bullet(
        "Todos los atributos son atómicos (monovalorados). No existen arreglos ni listas repetitivas.",
        bold_prefix="Cumplimiento 1FN: "
    )
    builder.add_bullet(
        "Está en 1FN y la clave primaria id_dispositivo es simple (consta de un solo atributo). Por definición matemática, "
        "al no existir claves compuestas, no pueden existir dependencias funcionales parciales.",
        bold_prefix="Cumplimiento 2FN: "
    )
    builder.add_bullet(
        "Está en 2FN y no existen dependencias transitivas entre atributos no primos. Se evitó explícitamente almacenar atributos como "
        "marca, categoria o nombre_modelo dentro de DISPOSITIVO, ya que habría generado la dependencia transitiva "
        "id_dispositivo -> id_modelo -> {marca, categoria}. Al aislar el concepto en la tabla MODELO_DISPOSITIVO, "
        "todo determinante no trivial X en X -> Y es una superclave (id_dispositivo o codigo_qr), cumpliendo rigurosamente 3FN y BCNF.",
        bold_prefix="Cumplimiento 3FN y BCNF: "
    )

    builder.add_h2("3.2. Normalización de LOTE")
    builder.add_body(
        "La entidad LOTE modela el conjunto de equipos declarados por un generador en una fecha determinada. "
        "Su clave primaria es id_lote y su clave alterna es codigo_lote.",
        bold_prefix="Definición de Claves: "
    )
    builder.add_bullet(
        "DF1: id_lote -> {codigo_lote, id_generador, id_solicitud, fecha_registro, cantidad_declarada, peso_declarado_kg, observaciones}\n"
        "DF2: codigo_lote -> {id_lote, id_generador, id_solicitud, fecha_registro, cantidad_declarada, peso_declarado_kg, observaciones}",
        bold_prefix="Dependencias Funcionales (DFs): "
    )
    builder.add_bullet(
        "Todos los atributos contienen valores escalares indivisibles. La lista de dispositivos individuales pertenecientes al lote "
        "no se almacena como un campo multivaluado en LOTE, sino mediante la clave foránea id_lote en DISPOSITIVO.",
        bold_prefix="Cumplimiento 1FN: "
    )
    builder.add_bullet(
        "La clave primaria id_lote es simple, por lo que todos los atributos no primos dependen por completo de la clave.",
        bold_prefix="Cumplimiento 2FN: "
    )
    builder.add_bullet(
        "No existen dependencias transitivas. Los atributos cantidad_declarada y peso_declarado_kg son independientes entre sí y describen "
        "exclusivamente al lote en cuestión. Los datos del generador (nombre, RUC, teléfono) residen en PERSONA y no se repiten en LOTE, "
        "garantizando 3FN y BCNF.",
        bold_prefix="Cumplimiento 3FN y BCNF: "
    )

    builder.add_h2("3.3. Normalización de EVALUACION_TECNICA")
    builder.add_body(
        "La entidad EVALUACION_TECNICA registra el diagnóstico especializado emitido por un técnico acreditado sobre un dispositivo.",
        bold_prefix="Definición de Claves: "
    )
    builder.add_bullet(
        "DF1: id_evaluacion -> {id_dispositivo, id_tecnico, id_clasificacion, diagnostico_funcional, diagnostico_estetico, fecha_evaluacion, aprobado_reutilizacion}",
        bold_prefix="Dependencias Funcionales (DFs): "
    )
    builder.add_bullet(
        "Atributos atómicos; los diagnósticos funcionales y estéticos son textos descriptivos individuales.",
        bold_prefix="Cumplimiento 1FN: "
    )
    builder.add_bullet(
        "Al tener como clave primaria un identificador simple (id_evaluacion), no hay dependencias parciales posibles.",
        bold_prefix="Cumplimiento 2FN: "
    )
    builder.add_bullet(
        "No existen dependencias transitivas. Se extrajo la clasificación técnica a la tabla CLASIFICACION_TECNICA para evitar que "
        "id_evaluacion -> id_clasificacion -> {nombre_clasificacion, permite_donacion}. De esta forma, el atributo permite_donacion depende "
        "únicamente del catálogo de clasificación y no se duplica en cada peritaje. Se cumple 3FN y BCNF.",
        bold_prefix="Cumplimiento 3FN y BCNF: "
    )

    builder.add_h2("3.4. Normalización de HISTORIAL_ESTADO (Entidad Débil)")
    builder.add_body(
        "HISTORIAL_ESTADO modela la línea de tiempo inmutable de transiciones de estado de cada residuo electrónico. "
        "Al ser una entidad débil, su Clave Primaria es Compuesta: {id_dispositivo, numero_secuencia}.",
        bold_prefix="Definición de Claves: "
    )
    builder.add_bullet(
        "DF1: {id_dispositivo, numero_secuencia} -> {id_estado, id_usuario, fecha_inicio, fecha_fin, observacion}\n"
        "DF2: id_dispositivo por sí solo NO determina id_estado (un equipo pasa por múltiples estados a lo largo del tiempo).\n"
        "DF3: numero_secuencia por sí solo NO determina nada (la secuencia 1 existe para todos los dispositivos).",
        bold_prefix="Dependencias Funcionales (DFs): "
    )
    builder.add_bullet(
        "Cada registro representa un único hito temporal indivisible.",
        bold_prefix="Cumplimiento 1FN: "
    )
    builder.add_bullet(
        "Al tener una clave primaria compuesta de dos atributos, debe verificarse rigurosamente que NINGÚN atributo no primo dependa "
        "de un subconjunto propio de la clave. Dado que id_estado, id_usuario, fecha_inicio, fecha_fin y observacion requieren "
        "conocer OBLIGATORIAMENTE tanto a cuál dispositivo pertenecen como en cuál secuencia ocurrieron, existe una Dependencia Funcional Completa. "
        "Por lo tanto, la tabla satisface plenamente la 2FN.",
        bold_prefix="Cumplimiento 2FN: "
    )
    builder.add_bullet(
        "No hay dependencias transitivas entre atributos no clave. El nombre del estado y el nombre del usuario se encuentran normalizados "
        "en ESTADO_DISPOSITIVO y USUARIO respectivamente. Ningún atributo no primo determina a otro atributo no primo. Cumple 3FN y BCNF.",
        bold_prefix="Cumplimiento 3FN y BCNF: "
    )

    builder.add_h2("3.5. Normalización de TRANSFERENCIA (MOVIMIENTO y DETALLE_MOVIMIENTO)")
    builder.add_body(
        "El traslado físico de residuos entre centros se descompone en dos entidades formalmente normalizadas: "
        "la cabecera de flete (MOVIMIENTO) y las líneas de carga de equipos (DETALLE_MOVIMIENTO), resolviendo la relación N:M entre "
        "fletes y dispositivos.",
        bold_prefix="Estructura de la Transferencia: "
    )
    builder.add_bullet(
        "En MOVIMIENTO: PK simple id_movimiento. DF1: id_movimiento -> {codigo_movimiento, id_centro_origen, id_centro_destino, id_responsable, id_estado_movimiento, fecha_salida, fecha_llegada, observaciones}. "
        "Cumple 1FN, 2FN y 3FN puesto que no almacena arreglos de dispositivos ni repite datos de los centros involucrados.\n"
        "En DETALLE_MOVIMIENTO (Entidad Débil): PK compuesta {id_movimiento, numero_linea}. "
        "DF1: {id_movimiento, numero_linea} -> {id_dispositivo, peso_kg_transferido}. "
        "DF2: {id_movimiento, id_dispositivo} -> {numero_linea, peso_kg_transferido} (Clave Alterna que evita duplicar un equipo en el mismo viaje).",
        bold_prefix="Dependencias Funcionales de Cabecera y Detalle: "
    )
    builder.add_bullet(
        "Tanto id_dispositivo como peso_kg_transferido dependen funcionalmente de la clave compuesta completa {id_movimiento, numero_linea}. "
        "El peso verificado al momento del embarque pertenece a ese flete específico y no solo al dispositivo de forma estática. "
        "No existen dependencias parciales (2FN) ni dependencias transitivas (3FN / BCNF).",
        bold_prefix="Cumplimiento 2FN y 3FN en la Carga: "
    )

    # SECCIÓN 4: SCRIPTS SQL Y PRUEBAS
    builder.add_h1("4. Implementación y Validación de Scripts SQL")
    builder.add_body(
        "Para garantizar la reproducibilidad técnica exigida en el proyecto integrador, la solución física se distribuye en cuatro archivos "
        "SQL totalmente compatibles con Microsoft SQL Server (T-SQL), estructurados de la siguiente manera:"
    )
    builder.add_bullet(
        "Crea la base de datos BD_ECORAEE_CLOUD y las 35 tablas normalizadas. Aplica restricciones declarativas PK, FK con políticas "
        "de integridad referencial (ON DELETE CASCADE selectivo y restrictivo por defecto), UNIQUE para claves alternas, NOT NULL, "
        "CHECK de validación de dominios físicos y reglas de negocio, valores por defecto DEFAULT e índices no agrupados de rendimiento.",
        bold_prefix="01_DDL.sql: "
    )
    builder.add_bullet(
        "Puebla todas las tablas con datos sintéticos realistas: 32 dispositivos electrónicos organizados en sus respectivos subtipos "
        "(Computadoras, Monitores, Tablets, Teléfonos, Routers y Periféricos) y cuatro ciclos de vida de trazabilidad completos desde "
        "el registro hasta el cierre terminal formal (Reutilizable en donación escolar, Reparable en taller, Reciclable con gestor calificado "
        "y No recuperable en confinamiento de seguridad).",
        bold_prefix="02_DML.sql: "
    )
    builder.add_bullet(
        "Contiene cinco pruebas de estrés de integridad que el motor SQL Server debe rechazar forzosamente: 1) PK repetida en entidad débil; "
        "2) FK inexistente; 3) UNIQUE repetido en código QR; 4) CHECK incumplido de peso negativo; y 5) Borrado de un registro padre que posee hijos asociados. "
        "Cada prueba cuenta con su justificación técnica y el código de error nativo arrojado por el motor.",
        bold_prefix="03_pruebas.sql: "
    )
    builder.add_bullet(
        "Implementa las cinco consultas analíticas y transaccionales del negocio requeridas en la rúbrica, empleando INNER/LEFT JOIN, "
        "agrupaciones GROUP BY con funciones agregadas (COUNT, SUM, AVG) y subconsultas escalares y correlacionadas (NOT IN y MAX(secuencia)).",
        bold_prefix="04_consultas.sql: "
    )

    # SECCIÓN 5: DECLARACIÓN DE USO DE IA
    builder.add_h1("5. Declaración de Uso de Inteligencia Artificial")
    builder.add_body(
        "En cumplimiento con la política institucional de integridad académica y transparencia tecnológica de la Universidad Internacional "
        "del Ecuador (UIDE) y las directrices docentes de la cátedra de Sistemas de Gestión de Bases de Datos, se declara de manera explícita "
        "el uso asistido de herramientas de Inteligencia Artificial generativa durante el desarrollo de esta entrega en los siguientes aspectos:"
    )
    builder.add_bullet(
        "Para validar la correcta concordancia sintáctica de sentencias T-SQL complejas en Microsoft SQL Server (tales como índices filtrados, "
        "declaración de claves compuestas en entidades débiles y subconsultas correlacionadas).",
        bold_prefix="1. Asistencia en Sintaxis y Buenas Prácticas SQL: "
    )
    builder.add_bullet(
        "Para acelerar la estructuración tipográfica y tabulación formal del Diccionario de Datos y la matriz relacional bajo el formato institucional UIDE.",
        bold_prefix="2. Formateo y Documentación Técnica: "
    )
    builder.add_bullet(
        "Para crear registros sintéticos plausibles y consistentes (marcas reales, números de serie simulados, procesadores y especificaciones "
        "de peso acordes al mercado tecnológico), asegurando la estricta ausencia de datos personales reales conforme a las restricciones del proyecto.",
        bold_prefix="3. Generación de Datos Sintéticos para el DML: "
    )
    builder.add_body(
        "El equipo de trabajo revisó, validó y ejecutó de forma crítica cada script y concepto técnico presentado, asumiendo la autoría y responsabilidad "
        "plena sobre el diseño arquitectónico, el modelo relacional y la solución entregada."
    )

    # SECCIÓN 6: EVIDENCIAS DE EJECUCIÓN DE SCRIPTS
    builder.add_h1("6. Evidencias de Ejecución de Scripts (Capturas SSMS)")
    builder.add_body(
        "A continuación se incorporan las evidencias de ejecución de los cuatro scripts en el motor Microsoft SQL Server (T-SQL) "
        "mediante SQL Server Management Studio (SSMS), demostrando la creación limpia de la base de datos, la carga masiva y los cuatro ciclos, "
        "la interceptación exitosa de las cinco restricciones de integridad y la resolución de las cinco consultas analíticas avanzadas."
    )
    
    cap_dir = r"c:\Users\nicol\OneDrive\Documentos\integrador 5to semestre\capturas"
    img_ddl = os.path.join(cap_dir, "ssms_01_ddl.png")
    img_dml = os.path.join(cap_dir, "ssms_02_dml.png")
    img_pruebas = os.path.join(cap_dir, "ssms_03_pruebas.png")
    img_consultas = os.path.join(cap_dir, "ssms_04_consultas.png")

    builder.add_h2("6.1. Ejecución de 01_DDL.sql (Creación de Base y Esquema)")
    builder.add_body(
        "Evidencia de compilación exitosa de 01_DDL.sql sin errores de sintaxis ni de dependencias, creando la base BD_ECORAEE_CLOUD "
        "y sus 35 tablas con restricciones declarativas completas."
    )
    if os.path.exists(img_ddl):
        add_figure_with_caption(builder.doc, img_ddl, "Figura 1. Salida de ejecución de 01_DDL.sql en SSMS: Commands completed successfully.")

    builder.add_h2("6.2. Ejecución de 02_DML.sql (Población de Datos y Ciclos Completos)")
    builder.add_body(
        "Evidencia de inserción de 32 dispositivos y los 4 ciclos completos de trazabilidad de extremo a extremo, confirmando el commit transaccional."
    )
    if os.path.exists(img_dml):
        add_figure_with_caption(builder.doc, img_dml, "Figura 2. Salida de ejecución de 02_DML.sql en SSMS: 32 dispositivos y 4 ciclos de trazabilidad cargados.")

    builder.add_h2("6.3. Ejecución de 03_pruebas.sql (Validación de Restricciones Rechazadas)")
    builder.add_body(
        "Evidencia de las cinco instrucciones rechazadas obligatoriamente por el motor (PK repetida, FK inexistente, UNIQUE duplicado, "
        "CHECK de masa negativa incumplido y violación de integridad referencial al intentar eliminar al técnico evaluador)."
    )
    if os.path.exists(img_pruebas):
        add_figure_with_caption(builder.doc, img_pruebas, "Figura 3. Salida de ejecución de 03_pruebas.sql en SSMS: Mensajes de error de restricción (Msg 2627 y Msg 547).")

    builder.add_h2("6.4. Ejecución de 04_consultas.sql (Cuadrículas de Resultados de Consultas)")
    builder.add_body(
        "Evidencia de los conjuntos de datos obtenidos (Results Grid) para las consultas A (historial), B (inventario por centro y estado), "
        "D (porcentaje de trazabilidad cerrada) y E (equipos en bodega pendientes de evaluación pericial)."
    )
    if os.path.exists(img_consultas):
        add_figure_with_caption(builder.doc, img_consultas, "Figura 4. Salida de ejecución de 04_consultas.sql en SSMS: Grids de resultados para las consultas avanzadas.")

    # REFERENCIAS APA 7MA EDICIÓN SIN NUMERAR
    builder.add_references_heading(lang="es")
    builder.add_apa_reference([
        ("Date, C. J. (2004). ", False),
        ("An Introduction to Database Systems", True),
        (" (8th ed.). Pearson Education.", False)
    ])
    builder.add_apa_reference([
        ("Elmasri, R., & Navathe, S. B. (2016). ", False),
        ("Fundamentals of Database Systems", True),
        (" (7th ed.). Pearson.", False)
    ])
    builder.add_apa_reference([
        ("Microsoft Corporation. (2026). ", False),
        ("Transact-SQL Reference (Database Engine) Documentation", True),
        (". Microsoft Learn. https://learn.microsoft.com/sql/t-sql/", False)
    ])
    builder.add_apa_reference([
        ("Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). ", False),
        ("Database System Concepts", True),
        (" (7th ed.). McGraw-Hill Education.", False)
    ])

    # Guardar en ambas ubicaciones
    out_path_1 = r"c:\Users\nicol\OneDrive\Documentos\integrador 5to semestre\Entrega_Fase2_Bases_de_Datos_EcoRAEE.docx"
    out_path_2 = r"C:\Users\nicol\Downloads\Scripts_Entrega_1_y_2\Entrega_Fase2_Bases_de_Datos_EcoRAEE.docx"
    
    builder.save(out_path_1)
    builder.save(out_path_2)
    print(f"Documento generado exitosamente en:\n1. {out_path_1}\n2. {out_path_2}")

if __name__ == "__main__":
    main()
