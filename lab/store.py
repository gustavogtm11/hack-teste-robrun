from __future__ import annotations

import csv
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from .catalog import DEMO_ITEMS


def app_data_dir() -> Path:
    base = Path.home() / "Documents" / "RobRunInventoryLab"
    base.mkdir(parents=True, exist_ok=True)
    return base


class InventoryStore:
    """A local-only model of server-side inventory authorization."""

    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or (app_data_dir() / "inventory_lab.sqlite3")
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    owned INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    action TEXT NOT NULL,
                    item_name TEXT NOT NULL,
                    result TEXT NOT NULL,
                    detail TEXT NOT NULL
                )
            """)
            count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
            if count == 0:
                conn.executemany(
                    "INSERT INTO items(id, name, category, rarity, owned) VALUES (?, ?, ?, ?, ?)",
                    DEMO_ITEMS,
                )
            conn.commit()

    def list_items(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, category, rarity, owned FROM items ORDER BY category, name"
            ).fetchall()
        return [dict(row) for row in rows]

    def _log(self, action: str, item_name: str, result: str, detail: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO audit(created_at, action, item_name, result, detail) VALUES (?, ?, ?, ?, ?)",
                (datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S"),
                 action, item_name, result, detail),
            )
            conn.commit()

    def request_item(self, item_name: str, client_claims_owned: bool = False) -> tuple[str, str]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT owned FROM items WHERE name = ?", (item_name,)
            ).fetchone()
        if row is None:
            detail = "Item inexistente no catálogo local; solicitação negada."
            self._log("REQUEST", item_name, "REJECTED", detail)
            return "REJECTED", detail

        # A claim supplied by a client is intentionally ignored. The authority
        # is the entitlement stored by this local server-side simulator.
        if client_claims_owned and not row["owned"]:
            detail = "A alegação do cliente foi ignorada. O servidor não encontrou propriedade válida."
            self._log("TAMPER_TEST", item_name, "REJECTED", detail)
            return "REJECTED", detail

        if not row["owned"]:
            detail = "Sem autorização: o item não consta como propriedade do perfil simulado."
            self._log("REQUEST", item_name, "REJECTED", detail)
            return "REJECTED", detail

        detail = "Propriedade confirmada pelo estado autoritativo local. Nenhum item foi criado ou alterado."
        self._log("REQUEST", item_name, "ACCEPTED", detail)
        return "ACCEPTED", detail

    def list_events(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT created_at, action, item_name, result, detail FROM audit ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def export_csv(self) -> Path:
        path = app_data_dir() / "inventory_audit.csv"
        rows = self.list_events(limit=100000)
        with path.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["created_at", "action", "item_name", "result", "detail"],
            )
            writer.writeheader()
            writer.writerows(rows)
        return path
