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
    path: Optional[Path] = typer.Option(None, help="Ruta donde crear el proyecto")
):
    """Crea un nuevo proyecto FastAPI con estructura completa"""
    
    console.print(f"\n[bold green]🚀 Creando proyecto '{name}'...[/bold green]\n")
    
    try:
        generator = ProjectGenerator(name, path)
        generator.generate()
        
        console.print(f"[bold green]✅ Proyecto '{name}' creado exitosamente![/bold green]\n")
        
        # Mostrar próximos pasos
        panel = Panel(
            f"""[yellow]1.[/yellow] cd {name}
[yellow]2.[/yellow] python -m venv venv
[yellow]3.[/yellow] source venv/bin/activate  [dim](Windows: venv\\Scripts\\activate)[/dim]
[yellow]4.[/yellow] pip install -r requirements.txt
[yellow]5.[/yellow] cp .env.example .env
[yellow]6.[/yellow] uvicorn app.main:app --reload""",
            title="[bold cyan]📝 Próximos pasos[/bold cyan]",
            border_style="cyan"
        )
        console.print(panel)
        
    except Exception as e:
        console.print(f"[bold red]❌ Error al crear proyecto: {e}[/bold red]")
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
        inspector = SQLInspector()
        inspector.connect()
        
        tables = inspector.get_tables()
        existing_models = inspector.get_existing_models()
        new_tables = [t for t in tables if t['name'] not in existing_models]
        
        if not new_tables:
            console.print("[green]✅ Todos los modelos están actualizados[/green]\n")
            raise typer.Exit(0)
        
        console.print(f"[yellow]📋 Se encontraron {len(new_tables)} tablas nuevas:[/yellow]")
        for table in new_tables:
            auth_marker = " [cyan](autenticación)[/cyan]" if inspector.is_auth_table(table['name']) else ""
            console.print(f"  ⚠ {table['name']}{auth_marker}")
        console.print()
        
        # Preguntas interactivas
        if not Confirm.ask("¿Desea generar modelos?", default=True):
            raise typer.Exit(0)
        
        console.print("\n[yellow]✨ Generando modelos...[/yellow]")
        model_gen = ModelGenerator()
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
            is_auth = inspector.is_auth_table(table['name'])
            controller_gen.generate(table, is_auth)
            console.print(f"  [green]✅[/green] app/controllers/{table['name']}_controller.py")
        
        if not Confirm.ask("\n¿Desea generar routes?", default=True):
            raise typer.Exit(0)
        
        console.print("\n[yellow]✨ Generando routes...[/yellow]")
        route_gen = RouteGenerator()
        for table in new_tables:
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
        
        console.print("\n[green]💡 Ejecuta 'uvicorn app.main:app --reload' para iniciar el servidor[/green]\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
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
def version():
    """Muestra la versión de Lara"""
    console.print(f"\n[bold cyan]Lara CLI[/bold cyan] version [green]{__version__}[/green]\n")


def main():
    """Punto de entrada principal"""
    app()


if __name__ == "__main__":
    main()
