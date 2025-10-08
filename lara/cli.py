"""CLI principal de Lara"""
import os
import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
from rich.panel import Panel
from typing import Optional

from lara.generators.project_generator import ProjectGenerator
from lara.generators.model_generator import ModelGenerator
from lara.generators.schema_generator import SchemaGenerator
from lara.generators.controller_generator import ControllerGenerator
from lara.generators.route_generator import RouteGenerator
from lara.generators.middleware_generator import MiddlewareGenerator
from lara.inspectors.sql_inspector import SQLInspector
from lara.__version__ import __version__

app = typer.Typer(
    name="lara",
    help="🚀 Lara - FastAPI CLI Generator para competencias de programación",
    add_completion=False
)
console = Console()


@app.command()
def create(
    name: str = typer.Argument(..., help="Nombre del proyecto"),
    path: Optional[Path] = typer.Option(None, help="Ruta donde crear el proyecto"),
    skip_setup: bool = typer.Option(False, "--skip-setup", help="Omitir configuración automática (venv, deps, .env)")
):
    """Crea un nuevo proyecto FastAPI con estructura completa y configuración automática"""
    
    console.print(f"\n[bold green]🚀 Creando proyecto '{name}'...[/bold green]\n")
    
    try:
        # 1. Generar estructura del proyecto
        generator = ProjectGenerator(name, path)
        project_path = generator.generate()
        
        console.print(f"[bold green]✅ Estructura del proyecto creada![/bold green]\n")
        
        if skip_setup:
            # Mostrar pasos manuales si se omite setup
            panel = Panel(
                f"""[yellow]1.[/yellow] cd {name}
[yellow]2.[/yellow] python -m venv venv
[yellow]3.[/yellow] source venv/bin/activate  [dim](Windows: venv\\Scripts\\activate)[/dim]
[yellow]4.[/yellow] pip install -r requirements.txt
[yellow]5.[/yellow] cp .env.example .env
[yellow]6.[/yellow] lara start""",
                title="[bold cyan]📝 Próximos pasos[/bold cyan]",
                border_style="cyan"
            )
            console.print(panel)
            return
        
        # 2. Pedir connection string (opcional para empezar sin BD)
        console.print("[cyan]🔌 Configuración de base de datos[/cyan]")
        console.print("[dim]Si no tienes una base de datos ahora, puedes dejarlo en blanco y configurarlo después.[/dim]\n")
        
        has_database = Confirm.ask("¿Deseas configurar una base de datos ahora?", default=True)
        connection_string = None
        
        if has_database:
            console.print("\n[cyan]💡 Ingresa el connection string de tu base de datos:[/cyan]")
            console.print("[dim]Ejemplos:[/dim]")
            console.print("[dim]  MongoDB: mongodb+srv://user:pass@cluster.mongodb.net/DB[/dim]")
            console.print("[dim]  SQL Server: Data Source=localhost\\SQLEXPRESS;Initial Catalog=DB;...[/dim]")
            console.print("[dim]  PostgreSQL: postgresql://user:pass@localhost:5432/db[/dim]")
            console.print("[dim]  MySQL: mysql://user:pass@localhost:3306/db[/dim]\n")
            
            connection_string = typer.prompt("Connection string", default="")
            
            if connection_string and connection_string.strip():
                connection_string = connection_string.strip()
            else:
                connection_string = None
                console.print("[yellow]⚠️  Sin base de datos - puedes configurarla después en .env[/yellow]\n")
        
        # 3. Configuración automática
        console.print("[yellow]⚙️  Configurando proyecto automáticamente...[/yellow]\n")
        
        import subprocess
        import sys
        from pathlib import Path
        
        project_dir = Path.cwd() / name
        
        # 3.1 Crear entorno virtual
        console.print("  [cyan]1/4[/cyan] Creando entorno virtual...")
        venv_result = subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        
        if venv_result.returncode == 0:
            console.print("      [green]✅ Entorno virtual creado[/green]")
        else:
            console.print("      [yellow]⚠️  No se pudo crear venv automáticamente[/yellow]")
        
        # 3.2 Determinar ejecutable de pip en el venv
        if sys.platform == "win32":
            pip_path = project_dir / "venv" / "Scripts" / "pip.exe"
            python_path = project_dir / "venv" / "Scripts" / "python.exe"
        else:
            pip_path = project_dir / "venv" / "bin" / "pip"
            python_path = project_dir / "venv" / "bin" / "python"
        
        # 3.3 Instalar dependencias
        console.print("  [cyan]2/4[/cyan] Instalando dependencias...")
        
        if pip_path.exists():
            pip_result = subprocess.run(
                [str(pip_path), "install", "-r", "requirements.txt", "--quiet"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if pip_result.returncode == 0:
                console.print("      [green]✅ Dependencias instaladas[/green]")
            else:
                console.print("      [yellow]⚠️  Algunas dependencias pueden no haberse instalado[/yellow]")
        else:
            console.print("      [yellow]⚠️  Instala manualmente: pip install -r requirements.txt[/yellow]")
        
        # 3.4 Configurar .env
        console.print("  [cyan]3/4[/cyan] Configurando .env...")
        
        env_example_path = project_dir / ".env.example"
        env_path = project_dir / ".env"
        
        if env_example_path.exists():
            # Leer .env.example
            with open(env_example_path, 'r') as f:
                env_content = f.read()
            
            # Si hay connection string, actualizar
            if connection_string:
                # Determinar qué variable usar
                is_mongodb = "mongodb" in connection_string.lower()
                
                if is_mongodb:
                    # Para MongoDB, activar las líneas correctas
                    env_content = env_content.replace('DATABASE_TYPE=sqlite', 'DATABASE_TYPE=mongodb')
                    env_content = env_content.replace(
                        '# MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/database_name?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true',
                        f'MONGODB_URL={connection_string}'
                    )
                    env_content = env_content.replace(
                        '# MONGODB_URL=mongodb://localhost:27017/database_name',
                        f'MONGODB_URL={connection_string}'
                    )
                    # Comentar SQLite
                    env_content = env_content.replace(
                        'DATABASE_URL=sqlite:///./app.db',
                        '# DATABASE_URL=sqlite:///./app.db'
                    )
                else:
                    # Para SQL, reemplazar DATABASE_URL
                    env_content = env_content.replace(
                        'DATABASE_URL=sqlite:///./app.db',
                        f'DATABASE_URL={connection_string}'
                    )
            
            # Escribir .env
            with open(env_path, 'w') as f:
                f.write(env_content)
            
            if connection_string:
                console.print("      [green]✅ .env configurado con tu base de datos[/green]")
            else:
                console.print("      [green]✅ .env creado (sin base de datos)[/green]")
        
        # 3.5 Mensaje final
        console.print("  [cyan]4/4[/cyan] Finalizando configuración...")
        console.print("      [green]✅ Proyecto completamente configurado![/green]\n")
        
        # Panel de éxito
        success_panel = Panel(
            f"""[bold green]✨ ¡Proyecto '{name}' listo para usar![/bold green]

[yellow]Para comenzar:[/yellow]
  cd {name}
  lara start

[dim]El entorno virtual se activará automáticamente.[/dim]""",
            title="[bold cyan]🎉 Configuración Completa[/bold cyan]",
            border_style="green"
        )
        console.print(success_panel)
        console.print()
        
    except subprocess.TimeoutExpired:
        console.print("\n[bold red]❌ Timeout instalando dependencias[/bold red]")
        console.print("[yellow]💡 Instala manualmente con: pip install -r requirements.txt[/yellow]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Error al crear proyecto: {e}[/bold red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]\n")
        raise typer.Exit(1)


@app.command(name="get-database")
def get_database(
    connection_string: Optional[str] = typer.Option(
        None, 
        "--connection", 
        "-c",
        help="Connection string de la base de datos (MongoDB o SQL)"
    )
):
    """Analiza la base de datos y muestra su estructura completa (SQL o MongoDB)"""
    
    console.print("\n[yellow]🔍 Analizando base de datos...[/yellow]\n")
    
    # Si no se proporciona por parámetro, pedir por terminal
    if not connection_string:
        # Intentar leer desde .env primero
        if Path(".env").exists():
            from dotenv import load_dotenv
            load_dotenv()
            connection_string = os.getenv("MONGODB_URL") or os.getenv("DATABASE_URL")
        
        # Si no hay en .env, pedir por terminal
        if not connection_string:
            console.print("[cyan]� Ingresa el connection string de tu base de datos:[/cyan]")
            console.print("[dim]Ejemplos:[/dim]")
            console.print("[dim]  MongoDB: mongodb+srv://user:pass@cluster.mongodb.net/DB[/dim]")
            console.print("[dim]  SQL Server: Data Source=localhost\\SQLEXPRESS;Initial Catalog=DB;...[/dim]")
            console.print("[dim]  PostgreSQL: postgresql://user:pass@localhost:5432/db[/dim]\n")
            
            connection_string = typer.prompt("Connection string")
            
            if not connection_string or connection_string.strip() == "":
                console.print("[bold red]❌ Connection string no puede estar vacío[/bold red]\n")
                raise typer.Exit(1)
    
    # Determinar qué inspector usar
    is_mongodb = (
        "mongodb" in connection_string.lower() or
        "mongodb+srv" in connection_string.lower()
    )
    
    try:
        if is_mongodb:
            # Usar MongoDB Inspector
            from lara.inspectors.mongodb_inspector import MongoDBInspector
            
            console.print("[cyan]🔌 Conectando a MongoDB...[/cyan]")
            inspector = MongoDBInspector(mongodb_url=connection_string)
            inspector.connect()
            
            # Información de la BD
            db_info = inspector.get_database_info()
            console.print(f"[green]✅ Conexión exitosa a MongoDB[/green]")
            console.print(f"   Cluster: {db_info['url']}")
            console.print(f"   Database: {db_info['name']}")
            console.print(f"   Colecciones: {db_info['collections_count']}\n")
            
            # Obtener colecciones
            collections = inspector.get_tables()
            
            if not collections:
                console.print("[red]❌ No se encontraron colecciones[/red]\n")
                raise typer.Exit(0)
            
            console.print(f"[green]✅ Se encontraron {len(collections)} colecciones:[/green]\n")
            
            # Mostrar cada colección
            for collection in collections:
                # Determinar si es colección de autenticación
                is_auth = inspector.is_auth_collection(collection['name'])
                has_pwd = inspector.has_password_field(collection)
                auth_emoji = "🔐 " if (is_auth or has_pwd) else ""
                
                # Crear tabla para mostrar campos
                fields_table = Table(
                    title=f"{auth_emoji}📋 {collection['name']} (Documents: {collection['document_count']})",
                    show_header=True,
                    header_style="bold cyan",
                    title_style="bold magenta" if (is_auth or has_pwd) else "bold white"
                )
                fields_table.add_column("Campo", style="yellow", width=20)
                fields_table.add_column("Tipo", style="blue", width=15)
                fields_table.add_column("Requerido", style="green", width=10, justify="center")
                fields_table.add_column("Notas", style="dim", width=30)
                
                for field in collection['columns']:
                    # Construir notas
                    notes = []
                    if field['primary_key']:
                        notes.append("PK")
                    if field.get('unique'):
                        notes.append("UNIQUE")
                    if field.get('foreign_key'):
                        notes.append(f"FK → {field['foreign_key_table']}")
                    if field['type'] == 'email':
                        notes.append("📧 Email")
                    if field['type'] == 'password':
                        notes.append("🔒 Password hash")
                    
                    fields_table.add_row(
                        field['name'],
                        field['python_type'],
                        "✅" if field['required'] else "❌",
                        ", ".join(notes) if notes else "─"
                    )
                
                console.print(fields_table)
                
                # Mostrar relaciones si existen
                if collection['relationships']:
                    console.print("[dim]  Relaciones detectadas:[/dim]")
                    for rel in collection['relationships']:
                        console.print(f"    🔗 {rel['field']} → {rel['target_collection']}.{rel['target_field']}")
                
                console.print()
            
            # Detectar si hay tabla de autenticación
            auth_collections = [c for c in collections if inspector.is_auth_collection(c['name']) or inspector.has_password_field(c)]
            if auth_collections:
                console.print(Panel(
                    f"[yellow]🔐 DETECCIÓN ESPECIAL:[/yellow]\n\n"
                    f"Se detectó colección de autenticación: [cyan]{auth_collections[0]['name']}[/cyan]\n"
                    f"Con [green]'lara sync-models'[/green] se generará automáticamente:\n"
                    f"  • Sistema completo de autenticación JWT\n"
                    f"  • Endpoints /register y /login\n"
                    f"  • Hash automático de contraseñas\n"
                    f"  • Middleware de autenticación",
                    title="[bold yellow]⚡ Sistema de Autenticación Disponible[/bold yellow]",
                    border_style="yellow"
                ))
                console.print()
            
        else:
            # Usar SQL Inspector
            console.print("[cyan]🔌 Conectando a base de datos SQL...[/cyan]")
            inspector = SQLInspector(database_url=connection_string)
            inspector.connect()
            
            # Información de la BD
            db_info = inspector.get_database_info()
            dialect_names = {
                'sqlite': 'SQLite',
                'postgresql': 'PostgreSQL',
                'mysql': 'MySQL',
                'mssql': 'Microsoft SQL Server'
            }
            db_name = dialect_names.get(db_info['type'], db_info['type'].upper())
            
            console.print(f"[green]✅ Conexión exitosa a {db_name}[/green]")
            if 'host' in db_info:
                console.print(f"   Host: {db_info['host']}")
            console.print(f"   Database: {db_info['database']}\n")
            
            # Obtener tablas
            tables = inspector.get_tables()
            
            if not tables:
                console.print("[red]❌ No se encontraron tablas[/red]\n")
                raise typer.Exit(0)
            
            console.print(f"[green]✅ Se encontraron {len(tables)} tablas:[/green]\n")
            
            # Mostrar cada tabla
            for table in tables:
                # Determinar si es tabla de autenticación
                is_auth = inspector.is_auth_table(table['name'])
                has_pwd = inspector.has_password_column(table)
                auth_emoji = "🔐 " if (is_auth or has_pwd) else ""
                
                # Obtener primary key
                pk_cols = [col['name'] for col in table['columns'] if col['primary_key']]
                pk_str = f"PK: {', '.join(pk_cols)}" if pk_cols else "Sin PK"
                
                # Crear tabla para mostrar columnas
                columns_table = Table(
                    title=f"{auth_emoji}📋 {table['name']} ({pk_str})",
                    show_header=True,
                    header_style="bold cyan",
                    title_style="bold magenta" if (is_auth or has_pwd) else "bold white"
                )
                columns_table.add_column("Columna", style="yellow", width=20)
                columns_table.add_column("Tipo", style="blue", width=20)
                columns_table.add_column("Nullable", style="green", width=10, justify="center")
                columns_table.add_column("Extra", style="dim", width=35)
                
                for col in table['columns']:
                    flags = []
                    if col['primary_key']:
                        flags.append("PK")
                    if col.get('autoincrement'):
                        flags.append("IDENTITY")
                    if col.get('foreign_key'):
                        flags.append(f"FK → {col['foreign_key']}")
                    if col.get('unique'):
                        flags.append("UNIQUE")
                    if col.get('default'):
                        flags.append(f"DEFAULT {col['default']}")
                    
                    # Detectar contraseñas
                    if 'password' in col['name'].lower():
                        flags.append("🔒 Password")
                    
                    columns_table.add_row(
                        col['name'],
                        col['type'],
                        "✅" if col['nullable'] else "❌",
                        ", ".join(flags) if flags else "─"
                    )
                
                console.print(columns_table)
                
                # Mostrar relaciones si existen
                if table['relationships']:
                    console.print("[dim]  Relaciones:[/dim]")
                    for rel in table['relationships']:
                        rel_type = "MANY TO ONE" if rel['type'] == 'many_to_one' else rel['type'].upper()
                        console.print(f"    🔗 {rel['foreign_key']} → {rel['target_table']}.{rel['target_column']} [{rel_type}]")
                
                console.print()
            
            # Detectar si hay tabla de autenticación
            auth_tables = [t for t in tables if inspector.is_auth_table(t['name']) or inspector.has_password_column(t)]
            if auth_tables:
                console.print(Panel(
                    f"[yellow]🔐 DETECCIÓN ESPECIAL:[/yellow]\n\n"
                    f"Se detectó tabla de autenticación: [cyan]{auth_tables[0]['name']}[/cyan]\n"
                    f"Con [green]'lara sync-models'[/green] se generará automáticamente:\n"
                    f"  • Sistema completo de autenticación JWT\n"
                    f"  • Endpoints /register y /login\n"
                    f"  • Hash automático de contraseñas\n"
                    f"  • Middleware de autenticación",
                    title="[bold yellow]⚡ Sistema de Autenticación Disponible[/bold yellow]",
                    border_style="yellow"
                ))
                console.print()
        
        # Detectar modelos faltantes (común para ambos)
        existing_models = inspector.get_existing_models()
        all_table_names = [t['name'] for t in (collections if is_mongodb else tables)]
        missing_tables = [name for name in all_table_names if name not in existing_models]
        
        if missing_tables:
            console.print(f"[yellow]⚠️  Se detectaron {len(missing_tables)} {'colecciones' if is_mongodb else 'tablas'} SIN modelos:[/yellow]")
            for table_name in missing_tables:
                console.print(f"  • {table_name}")
            console.print(f"\n[green]💡 Ejecuta 'lara sync-models' para generarlos automáticamente[/green]\n")
        else:
            console.print("[green]✅ Todos los modelos están sincronizados[/green]\n")
        
    except ValueError as e:
        console.print(f"[bold red]❌ {e}[/bold red]\n")
        raise typer.Exit(1)
    except ConnectionError as e:
        console.print(f"[bold red]❌ {e}[/bold red]\n")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Error inesperado: {e}[/bold red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]\n")
        raise typer.Exit(1)


@app.command(name="sync-models")
def sync_models():
    """Sincroniza modelos con la base de datos y genera código automáticamente"""
    
    console.print("\n[yellow]🔄 Sincronizando con base de datos...[/yellow]\n")
    
    try:
        # Detectar tipo de base de datos desde .env
        if Path(".env").exists():
            from dotenv import load_dotenv
            load_dotenv()
            
            mongodb_url = os.getenv("MONGODB_URL")
            database_url = os.getenv("DATABASE_URL")
            
            # Determinar qué inspector usar
            if mongodb_url or (database_url and "mongodb" in database_url.lower()):
                console.print("[cyan]🍃 Detectado: MongoDB[/cyan]")
                from lara.inspectors.mongodb_inspector import MongoDBInspector
                inspector = MongoDBInspector()
            else:
                console.print("[cyan]🗄️  Detectado: SQL Database[/cyan]")
                from lara.inspectors.sql_inspector import SQLInspector
                inspector = SQLInspector()
        else:
            # Sin .env, asumir SQL por defecto
            console.print("[yellow]⚠️  No se encontró .env, asumiendo SQL[/yellow]")
            from lara.inspectors.sql_inspector import SQLInspector
            inspector = SQLInspector()
        
        inspector.connect()
        
        tables = inspector.get_tables()
        existing_models = inspector.get_existing_models()
        new_tables = [t for t in tables if t['name'] not in existing_models]
        
        if not new_tables:
            console.print("[green]✅ Todos los modelos están actualizados[/green]\n")
            raise typer.Exit(0)
        
        console.print(f"[yellow]📋 Se encontraron {len(new_tables)} colecciones/tablas nuevas:[/yellow]")
        for table in new_tables:
            if hasattr(inspector, 'is_auth_collection'):
                auth_marker = " [cyan](autenticación)[/cyan]" if inspector.is_auth_collection(table['name']) else ""
            else:
                auth_marker = " [cyan](autenticación)[/cyan]" if inspector.is_auth_table(table['name']) else ""
            doc_count = table.get('document_count', table.get('row_count', 0))
            console.print(f"  ⚠ {table['name']}{auth_marker} ({doc_count} documentos)")
        console.print()
        
        # Preguntas interactivas
        if not Confirm.ask("¿Desea generar modelos?", default=True):
            raise typer.Exit(0)
        
        console.print("\n[yellow]✨ Generando modelos...[/yellow]")
        # Detectar si es MongoDB para usar el generador correcto
        is_mongodb = hasattr(inspector, 'is_auth_collection')
        db_type = 'mongodb' if is_mongodb else 'sql'
        model_gen = ModelGenerator(db_type=db_type)
        for table in new_tables:
            model_gen.generate(table)
            console.print(f"  [green]✅[/green] app/models/{table['name']}_model.py")
        
        if not Confirm.ask("\n¿Desea generar schemas Pydantic?", default=True):
            raise typer.Exit(0)
        
        console.print("\n[yellow]✨ Generando schemas...[/yellow]")
        schema_gen = SchemaGenerator()
        for table in new_tables:
            schema_gen.generate(table)
            console.print(f"  [green]✅[/green] app/schemas/{table['name']}_schema.py")
        
        if not Confirm.ask("\n¿Desea generar controllers CRUD?", default=True):
            raise typer.Exit(0)
        
        console.print("\n[yellow]✨ Generando controllers...[/yellow]")
        controller_gen = ControllerGenerator()
        for table in new_tables:
            if hasattr(inspector, 'is_auth_collection'):
                is_auth = inspector.is_auth_collection(table['name'])
            else:
                is_auth = inspector.is_auth_table(table['name'])
            controller_gen.generate(table, is_auth)
            console.print(f"  [green]✅[/green] app/controllers/{table['name']}_controller.py")
        
        if not Confirm.ask("\n¿Desea generar routes?", default=True):
            raise typer.Exit(0)
        
        console.print("\n[yellow]✨ Generando routes...[/yellow]")
        route_gen = RouteGenerator()
        for table in new_tables:
            if hasattr(inspector, 'is_auth_collection'):
                is_auth = inspector.is_auth_collection(table['name'])
            else:
                is_auth = inspector.is_auth_table(table['name'])
            route_gen.generate(table, is_auth)
            console.print(f"  [green]✅[/green] app/routes/{table['name']}_routes.py")
        
        # Actualizar main.py
        console.print("\n[yellow]🔧 Actualizando main.py...[/yellow]")
        route_gen.update_main(new_tables)
        console.print("  [green]✅[/green] Routers registrados automáticamente")
        
        # Resumen
        console.print("\n[bold green]🎉 ¡Sincronización completada![/bold green]\n")
        
        summary_panel = Panel(
            f"""• {len(new_tables)} modelos generados
• {len(new_tables) * 3} schemas generados (Create, Update, Response)
• {len(new_tables)} controllers generados
• {len(new_tables)} routers generados
• ~{len(new_tables) * 6} endpoints creados""",
            title="[bold cyan]📝 Resumen[/bold cyan]",
            border_style="cyan"
        )
        console.print(summary_panel)
        
        console.print("\n[green]💡 Ejecuta 'lara start' para iniciar el servidor[/green]\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]\n")
        raise typer.Exit(1)


@app.command(name="create-api")
def create_api(
    name: str = typer.Argument(..., help="Nombre del recurso (ej: producto, usuario)")
):
    """Genera modelo, schema, controller y routes para una API"""
    
    console.print(f"\n[yellow]✨ Creando API '{name}'...[/yellow]\n")
    
    # TODO: Implementar generación manual de API sin base de datos
    console.print("[yellow]⚠️  Este comando genera APIs basadas en base de datos existente[/yellow]")
    console.print("[yellow]💡 Usa 'lara sync-models' si tienes una tabla en la BD[/yellow]\n")
    
    raise typer.Exit(0)


@app.command(name="generate-middleware")
def generate_middleware(
    name: str = typer.Argument(..., help="Nombre del middleware")
):
    """Genera un middleware personalizado"""
    
    console.print(f"\n[yellow]✨ Generando middleware '{name}'...[/yellow]\n")
    
    try:
        generator = MiddlewareGenerator()
        output_path = generator.generate_custom_middleware(name)
        
        console.print(f"[green]✅ Middleware generado:[/green]")
        console.print(f"   {output_path}\n")
        
        console.print("[yellow]💡 No olvides registrar el middleware en main.py:[/yellow]")
        console.print(f"   [dim]from app.middlewares.{name}_middleware import {name.title().replace('_', '')}Middleware[/dim]")
        console.print(f"   [dim]app.add_middleware({name.title().replace('_', '')}Middleware)[/dim]\n")
        
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]\n")
        raise typer.Exit(1)


@app.command()
def start(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host del servidor"),
    port: int = typer.Option(8000, "--port", "-p", help="Puerto del servidor"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Auto-reload en cambios de código")
):
    """Inicia el servidor FastAPI con el entorno virtual activado"""
    
    import subprocess
    import sys
    from pathlib import Path
    
    console.print("\n[bold green]🚀 Iniciando servidor FastAPI...[/bold green]\n")
    
    # Verificar que estamos en un proyecto Lara
    if not Path("app/main.py").exists():
        console.print("[bold red]❌ No se encontró app/main.py[/bold red]")
        console.print("[yellow]💡 Asegúrate de estar en la raíz de tu proyecto Lara[/yellow]\n")
        raise typer.Exit(1)
    
    # Verificar si existe venv
    if sys.platform == "win32":
        python_path = Path("venv/Scripts/python.exe")
        activate_cmd = "venv\\Scripts\\activate"
    else:
        python_path = Path("venv/bin/python")
        activate_cmd = "source venv/bin/activate"
    
    if not python_path.exists():
        console.print("[yellow]⚠️  No se encontró entorno virtual[/yellow]")
        console.print(f"[yellow]💡 Ejecuta: python -m venv venv && {activate_cmd}[/yellow]\n")
        # Intentar con python del sistema
        python_path = sys.executable
    
    # Construir comando uvicorn
    reload_flag = "--reload" if reload else ""
    
    try:
        console.print(f"[cyan]🌐 Servidor corriendo en: [bold]http://{host}:{port}[/bold][/cyan]")
        console.print(f"[cyan]📚 Documentación en: [bold]http://{host}:{port}/docs[/bold][/cyan]")
        console.print(f"[dim]Presiona Ctrl+C para detener el servidor[/dim]\n")
        console.print("─" * 70)
        console.print()
        
        # Ejecutar uvicorn
        cmd = [
            str(python_path),
            "-m",
            "uvicorn",
            "app.main:app",
            "--host", host,
            "--port", str(port)
        ]
        
        if reload:
            cmd.append("--reload")
        
        # Ejecutar en modo interactivo para ver logs
        subprocess.run(cmd, cwd=Path.cwd())
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Servidor detenido por el usuario[/yellow]\n")
    except FileNotFoundError:
        console.print("\n[bold red]❌ No se encontró uvicorn[/bold red]")
        console.print("[yellow]💡 Instala dependencias: pip install -r requirements.txt[/yellow]\n")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error al iniciar servidor: {e}[/bold red]\n")
        raise typer.Exit(1)


@app.command()
def version():
    """Muestra la versión de Lara"""
    console.print(f"\n[bold cyan]Lara CLI[/bold cyan] version [green]{__version__}[/green]\n")


def main():
    """Punto de entrada principal"""
    app()


if __name__ == "__main__":
    main()
