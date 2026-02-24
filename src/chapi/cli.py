import click


@click.group()
def cli() -> None: ...


@cli.command()
def version() -> None:
    from chapi import __version__

    click.echo(__version__)
