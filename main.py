import asyncio
from meshview import web

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            web.run_server()
        )

def cli_main():
    """Entry point for console script."""
    asyncio.run(main())

if __name__ == '__main__':
    cli_main()
