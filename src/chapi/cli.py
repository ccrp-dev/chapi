import click


@click.group()
def cli() -> None: ...


@cli.command()
def version() -> None:
    from chapi import __version__

    click.echo(__version__)


@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
@click.option(
    '--log-level',
    default='info',
    type=click.Choice(['critical', 'error', 'warning', 'info', 'debug', 'trace']),
    help='Log level',
)
def serve(host: str, port: int, log_level: str) -> None:
    """Run the FastAPI application with uvicorn."""
    import uvicorn

    from chapi.api.app import get_app

    app = get_app()

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=log_level,
    )
