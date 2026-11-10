"""Wait for the writer app while it runs long migrations instead of giving up."""

import pytest

from meshview import migrations


def _patch(monkeypatch, states):
    """Feed (up_to_date, in_progress) pairs, one per check."""
    states = iter(states)
    current = {}

    async def is_up_to_date(engine, database_url):
        current["up_to_date"], current["in_progress"] = next(states)
        return current["up_to_date"]

    async def in_progress(engine):
        return current["in_progress"]

    async def revision(*args):
        return None

    async def no_sleep(delay):
        pass

    monkeypatch.setattr(migrations, "is_database_up_to_date", is_up_to_date)
    monkeypatch.setattr(migrations, "is_migration_in_progress", in_progress)
    monkeypatch.setattr(migrations, "get_current_revision", revision)
    monkeypatch.setattr(migrations, "get_head_revision", revision)
    monkeypatch.setattr(migrations.asyncio, "sleep", no_sleep)


@pytest.mark.asyncio
async def test_migration_in_progress_does_not_use_retries(monkeypatch):
    _patch(monkeypatch, [(False, True)] * 50 + [(True, False)])
    assert await migrations.wait_for_migrations(None, "", max_retries=3, retry_delay=0)


@pytest.mark.asyncio
async def test_gives_up_when_no_migration_is_running(monkeypatch):
    _patch(monkeypatch, [(False, False)] * 3 + [(True, False)])
    assert not await migrations.wait_for_migrations(None, "", max_retries=3, retry_delay=0)


@pytest.mark.asyncio
async def test_retries_count_only_while_idle(monkeypatch):
    states = [(False, False), (False, True), (False, True), (False, False), (True, False)]
    _patch(monkeypatch, states)
    assert await migrations.wait_for_migrations(None, "", max_retries=3, retry_delay=0)
