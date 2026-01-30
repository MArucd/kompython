import asyncio

import click
from sqlalchemy import delete, select

from database import AsyncSessionLocal
from models import Products, Source


@click.group()
def cli():
    pass


@cli.command()
def clean():
    async def _clean():
        async with AsyncSessionLocal() as session:
            try:
                click.echo("Cleaning database...")
                await session.execute(delete(Products))
                await session.execute(delete(Source))
                await session.commit()
                click.echo("Database cleaned!")
            except Exception as e:
                await session.rollback()
                click.echo(f"Error: {e}")

    asyncio.run(_clean())


@cli.command()
@click.option("--domain", help="Clean only specific domain")
def clean_sources(domain):
    async def _clean_sources():
        async with AsyncSessionLocal() as session:
            try:
                if domain:
                    await session.execute(delete(Source).where(Source.domain == domain))
                    click.echo(f"Source for domain '{domain}' deleted")
                else:
                    await session.execute(delete(Source))
                    click.echo("All sources deleted")
                await session.commit()
            except Exception as e:
                await session.rollback()
                click.echo(f"Error: {e}")

    asyncio.run(_clean_sources())


@cli.command()
def stats():
    async def _stats():
        async with AsyncSessionLocal() as session:
            try:
                sources_result = await session.execute(select(Source))
                sources_count = len(sources_result.scalars().all())

                products_result = await session.execute(select(Products))
                products_count = len(products_result.scalars().all())

                click.echo("Database Statistics:")
                click.echo(f"   Sources: {sources_count}")
                click.echo(f"   Products: {products_count}")
            except Exception as e:
                click.echo(f"Error: {e}")

    asyncio.run(_stats())


@cli.command()
@click.option("--limit", default=5, help="Limit records")
def inspect(limit):
    async def _inspect():
        async with AsyncSessionLocal() as session:
            try:
                sources_result = await session.execute(select(Source))
                sources = sources_result.scalars().all()
                click.echo(f"SOURCES ({len(sources)}):")
                for source in sources:
                    click.echo(f"  {source.domain}")

                products_result = await session.execute(select(Products))
                products = products_result.scalars().all()
                click.echo(f"\nPRODUCTS ({len(products)}):")
                for product in products[:limit]:
                    click.echo(f"  {product.origin}: {product.name}")
                if len(products) > limit:
                    click.echo(f"  ... and {len(products) - limit} more")
            except Exception as e:
                click.echo(f"Error: {e}")

    asyncio.run(_inspect())


if __name__ == "__main__":
    cli()
