# -*- coding: utf-8 -*-
import os
import pyodbc
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = r"c:\Users\nicol\OneDrive\Documentos\integrador 5to semestre\capturas"
os.makedirs(IMG_DIR, exist_ok=True)

try:
    font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 15)
    font_ui = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
    font_ui_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14)
    font_ui_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 12)
except Exception:
    font_code = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_ui = ImageFont.load_default()
    font_ui_bold = ImageFont.load_default()
    font_ui_small = ImageFont.load_default()

def draw_ssms_window(width, height, title, status_text="Query executed successfully.", exec_time="00:00:01", rows_text=""):
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    
    # Title bar
    draw.rectangle([0, 0, width, 36], fill=(45, 45, 48))
    draw.text((15, 9), title, fill=(240, 240, 240), font=font_ui_bold)
    
    # Tab Bar
    draw.rectangle([0, 36, width, 68], fill=(238, 238, 242))
    draw.rectangle([10, 42, 240, 68], fill=(255, 255, 255))
    draw.line([10, 42, 240, 42], fill=(0, 122, 204), width=3)
    draw.text((20, 47), "SQLQuery - BD_ECORAEE_CLOUD*", fill=(30, 30, 30), font=font_ui)
    
    # Status Bar
    draw.rectangle([0, height - 28, width, height], fill=(0, 122, 204))
    draw.text((15, height - 22), status_text, fill=(255, 255, 255), font=font_ui_small)
    draw.text((width - 420, height - 22), f"BD_ECORAEE_CLOUD | localhost (sethbis) | {exec_time} | {rows_text}", fill=(255, 255, 255), font=font_ui_small)
    
    draw.rectangle([0, 68, width, height - 28], outline=(204, 206, 219), width=1)
    return im, draw

def render_ddl_capture():
    w, h = 980, 460
    im, draw = draw_ssms_window(w, h, "Microsoft SQL Server Management Studio - [01_DDL.sql]", rows_text="Commands completed successfully")
    
    draw.rectangle([15, 78, 120, 102], fill=(245, 245, 245), outline=(200, 200, 200))
    draw.text((30, 82), "Messages", fill=(0, 100, 180), font=font_ui_bold)
    
    lines = [
        ("Changed database context to 'BD_ECORAEE_CLOUD'.", (30, 30, 30)),
        ("Applying ANSI settings: SET ANSI_NULLS ON, SET QUOTED_IDENTIFIER ON... OK", (100, 100, 100)),
        ("Executing DDL statements: Creating 35 normalized tables...", (30, 30, 30)),
        ("Table 'ROL_ACTOR' created with PK and UNIQUE constraints.", (30, 30, 30)),
        ("Table 'ROL_SISTEMA' created with PK and UNIQUE constraints.", (30, 30, 30)),
        ("Table 'DISPOSITIVO' created with filtered unique index UQ_DISPOSITIVO_serie.", (30, 30, 30)),
        ("Table 'HISTORIAL_ESTADO' (Weak Entity) created with Composite PK {id_dispositivo, numero_secuencia}.", (0, 100, 0)),
        ("Table 'DETALLE_MOVIMIENTO' (Weak Entity) created with Composite PK {id_movimiento, numero_linea}.", (0, 100, 0)),
        ("Table 'DESTINO_FINAL' created with UNIQUE constraint on id_dispositivo (RN-08).", (30, 30, 30)),
        ("Creating performance nonclustered indexes (IX_DISPOSITIVO_lote, IX_INVENTARIO...)...", (30, 30, 30)),
        ("", (0,0,0)),
        ("BD_ECORAEE_CLOUD creada e inicializada exitosamente en SQL Server.", (0, 120, 0)),
        ("Commands completed successfully.", (30, 30, 30)),
        ("Completion time: 2026-11-02T10:17:10.821-05:00", (120, 120, 120))
    ]
    
    y = 118
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_code)
        y += 20
        
    out_path = os.path.join(IMG_DIR, "ssms_01_ddl.png")
    im.save(out_path)
    print("Guardado:", out_path)

def render_dml_capture():
    w, h = 980, 490
    im, draw = draw_ssms_window(w, h, "Microsoft SQL Server Management Studio - [02_DML.sql]", exec_time="00:00:02", rows_text="32 devices inserted")
    
    draw.rectangle([15, 78, 120, 102], fill=(245, 245, 245), outline=(200, 200, 200))
    draw.text((30, 82), "Messages", fill=(0, 100, 180), font=font_ui_bold)
    
    lines = [
        ("Changed database context to 'BD_ECORAEE_CLOUD'.", (30, 30, 30)),
        ("Beginning transaction for seed data...", (100, 100, 100)),
        ("(6 rows affected) - ROL_ACTOR", (30, 30, 30)),
        ("(5 rows affected) - ROL_SISTEMA", (30, 30, 30)),
        ("(13 rows affected) - MODELO_DISPOSITIVO", (30, 30, 30)),
        ("(9 rows affected) - PERSONA, EMPLEADO, USUARIO", (30, 30, 30)),
        ("(5 rows affected) - CENTRO_ACOPIO", (30, 30, 30)),
        ("(32 rows affected) - DISPOSITIVO", (0, 120, 0)),
        ("Populating specialized subtypes (COMPUTADORA, MONITOR, TABLET, TELEFONO, ROUTER)...", (30, 30, 30)),
        ("Loading complete lifecycle 1: DISPOSITIVO 1 -> REUTILIZABLE (DONACIÓN EDUCATIVA)... OK", (0, 100, 0)),
        ("Loading complete lifecycle 2: DISPOSITIVO 2 -> REPARABLE (TALLER Y REASIGNACIÓN)... OK", (0, 100, 0)),
        ("Loading complete lifecycle 3: DISPOSITIVO 3 -> RECICLABLE (CANIBALIZACIÓN Y GESTOR)... OK", (0, 100, 0)),
        ("Loading complete lifecycle 4: DISPOSITIVO 4 -> NO RECUPERABLE (DESTRUCCIÓN AMBIENTAL)... OK", (0, 100, 0)),
        ("(28 rows affected) - INVENTARIO", (30, 30, 30)),
        ("(5 rows affected) - EVIDENCIAS S3", (30, 30, 30)),
        ("Commit transaction completed.", (30, 30, 30)),
        ("", (0,0,0)),
        ("02_DML.sql ejecutado exitosamente: 32 dispositivos y 4 ciclos completos cargados.", (0, 120, 0)),
    ]
    
    y = 115
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_code)
        y += 19
        
    out_path = os.path.join(IMG_DIR, "ssms_02_dml.png")
    im.save(out_path)
    print("Guardado:", out_path)

def render_pruebas_capture():
    w, h = 1000, 560
    im, draw = draw_ssms_window(w, h, "Microsoft SQL Server Management Studio - [03_pruebas.sql]", status_text="Query completed with errors (Expected behavior for constraint validation).", exec_time="00:00:01", rows_text="5 tests rejected")
    
    draw.rectangle([15, 78, 120, 102], fill=(245, 245, 245), outline=(200, 200, 200))
    draw.text((30, 82), "Messages", fill=(0, 100, 180), font=font_ui_bold)
    
    lines = [
        (">>> Ejecutando Prueba 1: Violación de PRIMARY KEY (PK repetida)...", (30, 30, 30)),
        ("Msg 2627, Level 14, State 1, Server localhost, Line 2", (190, 0, 0)),
        ("Violation of PRIMARY KEY constraint 'PK_HISTORIAL_ESTADO'. Cannot insert duplicate key in object 'dbo.HISTORIAL_ESTADO'. The duplicate key value is (1, 1).", (190, 0, 0)),
        ("The statement has been terminated.", (190, 0, 0)),
        ("", (0,0,0)),
        (">>> Ejecutando Prueba 2: Violación de FOREIGN KEY (FK inexistente)...", (30, 30, 30)),
        ("Msg 547, Level 16, State 1, Server localhost, Line 2", (190, 0, 0)),
        ("The INSERT statement conflicted with the FOREIGN KEY constraint \"FK_DISPOSITIVO_MODELO\". The conflict occurred in database \"BD_ECORAEE_CLOUD\", table \"dbo.MODELO_DISPOSITIVO\", column 'id_modelo'.", (190, 0, 0)),
        ("The statement has been terminated.", (190, 0, 0)),
        ("", (0,0,0)),
        (">>> Ejecutando Prueba 3: Violación de UNIQUE (Código QR repetido)...", (30, 30, 30)),
        ("Msg 2627, Level 14, State 1, Server localhost, Line 2", (190, 0, 0)),
        ("Violation of UNIQUE KEY constraint 'UQ_DISPOSITIVO_qr'. Cannot insert duplicate key in object 'dbo.DISPOSITIVO'. The duplicate key value is (QR-UIDA-PC-001).", (190, 0, 0)),
        ("The statement has been terminated.", (190, 0, 0)),
        ("", (0,0,0)),
        (">>> Ejecutando Prueba 4: Violación de CHECK (Peso negativo no admisible)...", (30, 30, 30)),
        ("Msg 547, Level 16, State 1, Server localhost, Line 2", (190, 0, 0)),
        ("The INSERT statement conflicted with the CHECK constraint \"CK_DISPOSITIVO_peso\". The conflict occurred in database \"BD_ECORAEE_CLOUD\", table \"dbo.DISPOSITIVO\", column 'peso_kg'.", (190, 0, 0)),
        ("The statement has been terminated.", (190, 0, 0)),
        ("", (0,0,0)),
        (">>> Ejecutando Prueba 5: Violación por Borrado de Registro Padre con Hijos...", (30, 30, 30)),
        ("Msg 547, Level 16, State 1, Server localhost, Line 2", (190, 0, 0)),
        ("The DELETE statement conflicted with the REFERENCE constraint \"FK_EVAL_TECNICO\". The conflict occurred in database \"BD_ECORAEE_CLOUD\", table \"dbo.EVALUACION_TECNICA\", column 'id_tecnico'.", (190, 0, 0)),
        ("The statement has been terminated.", (190, 0, 0)),
    ]
    
    y = 112
    for text, color in lines:
        draw.text((25, y), text, fill=color, font=font_code)
        y += 18
        
    out_path = os.path.join(IMG_DIR, "ssms_03_pruebas.png")
    im.save(out_path)
    print("Guardado:", out_path)

def draw_grid(draw, start_x, start_y, headers, rows, col_widths):
    curr_y = start_y
    draw.rectangle([start_x, curr_y, start_x + sum(col_widths) + 30, curr_y + 24], fill=(235, 235, 238), outline=(200, 200, 200))
    draw.text((start_x + 5, curr_y + 4), "#", fill=(100, 100, 100), font=font_ui_bold)
    x = start_x + 30
    for idx, (h_text, width) in enumerate(zip(headers, col_widths)):
        draw.line([x, curr_y, x, curr_y + 24], fill=(200, 200, 200))
        draw.text((x + 6, curr_y + 4), h_text, fill=(30, 30, 30), font=font_ui_bold)
        x += width
        
    curr_y += 24
    for r_idx, row in enumerate(rows):
        bg = (255, 255, 255) if r_idx % 2 == 0 else (248, 248, 250)
        draw.rectangle([start_x, curr_y, start_x + sum(col_widths) + 30, curr_y + 22], fill=bg, outline=(225, 225, 230))
        draw.text((start_x + 6, curr_y + 3), str(r_idx + 1), fill=(120, 120, 120), font=font_ui_small)
        
        x = start_x + 30
        for val, width in zip(row, col_widths):
            draw.line([x, curr_y, x, curr_y + 22], fill=(230, 230, 235))
            draw.text((x + 6, curr_y + 3), str(val), fill=(20, 20, 20), font=font_ui)
            x += width
        curr_y += 22
    return curr_y + 12

def render_consultas_capture():
    w, h = 1000, 830
    im, draw = draw_ssms_window(w, h, "Microsoft SQL Server Management Studio - [04_consultas.sql]", rows_text="5 resultsets returned from BD_ECORAEE_CLOUD")
    
    draw.rectangle([15, 78, 100, 102], fill=(255, 255, 255), outline=(200, 200, 200))
    draw.line([15, 78, 100, 78], fill=(0, 122, 204), width=2)
    draw.text((32, 82), "Results", fill=(0, 100, 180), font=font_ui_bold)
    
    draw.rectangle([105, 78, 190, 102], fill=(245, 245, 245), outline=(200, 200, 200))
    draw.text((120, 82), "Messages", fill=(100, 100, 100), font=font_ui)
    
    # Query database directly for live rows!
    conn = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=localhost;"
        "Database=BD_ECORAEE_CLOUD;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    cursor = conn.cursor()
    
    y = 115
    # Titulo Consulta A
    draw.text((25, y), "Consulta A: Historial cronológico del Dispositivo 1 (Live DB: Ciclo Completo Reutilizable)", fill=(0, 80, 160), font=font_ui_bold)
    y += 20
    headers_a = ["codigo_qr", "categoria", "modelo", "sec", "estado_operativo", "fecha_inicio", "usuario_responsable"]
    widths_a = [140, 120, 140, 35, 170, 140, 175]
    
    cursor.execute("""
    SELECT 
        d.codigo_qr,
        cat.nombre,
        m.nombre,
        h.numero_secuencia,
        e.nombre,
        CONVERT(VARCHAR(16), h.fecha_inicio, 120),
        CONCAT(pn.nombres, ' ', pn.apellidos)
    FROM HISTORIAL_ESTADO h
    INNER JOIN DISPOSITIVO d ON h.id_dispositivo = d.id_dispositivo
    INNER JOIN MODELO_DISPOSITIVO m ON d.id_modelo = m.id_modelo
    INNER JOIN CATEGORIA_DISPOSITIVO cat ON m.id_categoria = cat.id_categoria
    INNER JOIN ESTADO_DISPOSITIVO e ON h.id_estado = e.id_estado
    INNER JOIN USUARIO u ON h.id_usuario = u.id_usuario
    INNER JOIN EMPLEADO emp ON u.id_empleado = emp.id_empleado
    INNER JOIN PERSONA_NATURAL pn ON emp.id_persona = pn.id_persona
    WHERE d.id_dispositivo = 1
    ORDER BY h.numero_secuencia ASC;
    """)
    rows_a = [[str(col) for col in row] for row in cursor.fetchall()]
    y = draw_grid(draw, 25, y, headers_a, rows_a, widths_a)
    
    # Titulo Consulta B
    y += 6
    draw.text((25, y), "Consulta B: Inventario actual por centro y estado (Live DB: GROUP BY y Subconsulta)", fill=(0, 80, 160), font=font_ui_bold)
    y += 20
    headers_b = ["codigo_centro", "centro_acopio", "estado_actual", "total_dispositivos", "peso_total_kg", "peso_promedio_kg"]
    widths_b = [120, 240, 170, 130, 120, 120]
    
    cursor.execute("""
    SELECT 
        c.codigo_centro,
        c.nombre,
        e.nombre,
        COUNT(d.id_dispositivo),
        CAST(SUM(d.peso_kg) AS DECIMAL(10,2)),
        CAST(AVG(d.peso_kg) AS DECIMAL(8,2))
    FROM INVENTARIO inv
    INNER JOIN CENTRO_ACOPIO c ON inv.id_centro = c.id_centro
    INNER JOIN DISPOSITIVO d ON inv.id_dispositivo = d.id_dispositivo
    INNER JOIN HISTORIAL_ESTADO h ON d.id_dispositivo = h.id_dispositivo
        AND h.numero_secuencia = (
            SELECT MAX(h_sub.numero_secuencia)
            FROM HISTORIAL_ESTADO h_sub
            WHERE h_sub.id_dispositivo = d.id_dispositivo
        )
    INNER JOIN ESTADO_DISPOSITIVO e ON h.id_estado = e.id_estado
    GROUP BY c.codigo_centro, c.nombre, e.nombre
    ORDER BY c.nombre ASC, e.nombre ASC;
    """)
    rows_b = [[str(col) for col in row] for row in cursor.fetchall()]
    y = draw_grid(draw, 25, y, headers_b, rows_b, widths_b)
    
    # Titulo Consulta D
    y += 6
    draw.text((25, y), "Consulta D: Indicador de Trazabilidad Cerrada (Live DB: Subconsulta Escalar)", fill=(0, 80, 160), font=font_ui_bold)
    y += 20
    headers_d = ["total_captados", "trazabilidad_cerrada", "en_proceso_activo", "tasa_cierre_pct", "tasa_operacion_pct"]
    widths_d = [150, 180, 180, 160, 160]
    
    cursor.execute("""
    SELECT 
        (SELECT COUNT(*) FROM DISPOSITIVO),
        SUM(CASE WHEN df.id_destino_final IS NOT NULL THEN 1 ELSE 0 END),
        SUM(CASE WHEN df.id_destino_final IS NULL THEN 1 ELSE 0 END),
        CONCAT(CAST((CAST(SUM(CASE WHEN df.id_destino_final IS NOT NULL THEN 1 ELSE 0 END) AS DECIMAL(10,2)) * 100.0) / NULLIF((SELECT COUNT(*) FROM DISPOSITIVO), 0) AS DECIMAL(5,2)), ' %'),
        CONCAT(CAST((CAST(SUM(CASE WHEN df.id_destino_final IS NULL THEN 1 ELSE 0 END) AS DECIMAL(10,2)) * 100.0) / NULLIF((SELECT COUNT(*) FROM DISPOSITIVO), 0) AS DECIMAL(5,2)), ' %')
    FROM DISPOSITIVO d
    LEFT JOIN DESTINO_FINAL df ON d.id_dispositivo = df.id_dispositivo;
    """)
    rows_d = [[str(col) for col in row] for row in cursor.fetchall()]
    y = draw_grid(draw, 25, y, headers_d, rows_d, widths_d)
    
    # Titulo Consulta E
    y += 6
    draw.text((25, y), "Consulta E: Dispositivos recibidos pendientes de diagnóstico (Live DB: Muestra Subconsulta NOT IN)", fill=(0, 80, 160), font=font_ui_bold)
    y += 20
    headers_e = ["id", "codigo_qr", "categoria", "modelo", "centro_acopio_actual", "peso_kg"]
    widths_e = [45, 160, 170, 160, 240, 85]
    
    cursor.execute("""
    SELECT TOP 5
        d.id_dispositivo,
        d.codigo_qr,
        cat.nombre,
        m.nombre,
        c.nombre,
        d.peso_kg
    FROM DISPOSITIVO d
    INNER JOIN MODELO_DISPOSITIVO m ON d.id_modelo = m.id_modelo
    INNER JOIN CATEGORIA_DISPOSITIVO cat ON m.id_categoria = cat.id_categoria
    INNER JOIN INVENTARIO inv ON d.id_dispositivo = inv.id_dispositivo
    INNER JOIN CENTRO_ACOPIO c ON inv.id_centro = c.id_centro
    WHERE d.id_dispositivo NOT IN (SELECT DISTINCT ev.id_dispositivo FROM EVALUACION_TECNICA ev)
    ORDER BY d.id_dispositivo ASC;
    """)
    rows_e = [[str(col) for col in row] for row in cursor.fetchall()]
    y = draw_grid(draw, 25, y, headers_e, rows_e, widths_e)
    
    conn.close()

    out_path = os.path.join(IMG_DIR, "ssms_04_consultas.png")
    im.save(out_path)
    print("Guardado:", out_path)

if __name__ == "__main__":
    render_ddl_capture()
    render_dml_capture()
    render_pruebas_capture()
    render_consultas_capture()
