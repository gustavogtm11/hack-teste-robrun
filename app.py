from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

from lab.store import InventoryStore

APP_NAME = "ROB RUN | Inventory Security Lab"


class InventoryLabApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1020x700")
        self.root.minsize(850, 580)
        self.store = InventoryStore()
        self._style()
        self._build()
        self.refresh()

    def _style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#101722")
        style.configure("TLabel", background="#101722", foreground="#e8eef7", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#ffffff")
        style.configure("Muted.TLabel", foreground="#9aabc0")
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Treeview", rowheight=29, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build(self) -> None:
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x")
        ttk.Label(header, text="Inventory Security Lab", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Ambiente local de pesquisa. Nenhuma conexão com ROB RUN ou servidores externos.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        toolbar = ttk.Frame(outer)
        toolbar.pack(fill="x", pady=(0, 12))
        ttk.Label(toolbar, text="Equipamento:").pack(side="left")
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(toolbar, textvariable=self.item_var, state="readonly", width=34)
        self.item_combo.pack(side="left", padx=(8, 12))
        ttk.Button(toolbar, text="Solicitar item (teste legítimo)", command=self.request_item).pack(side="left")
        ttk.Button(toolbar, text="Simular requisição adulterada", command=self.tamper_request).pack(side="left", padx=8)
        ttk.Button(toolbar, text="Atualizar", command=self.refresh).pack(side="right")

        content = ttk.Panedwindow(outer, orient="vertical")
        content.pack(fill="both", expand=True)

        inventory_frame = ttk.Labelframe(content, text="Inventário local simulado", padding=10)
        audit_frame = ttk.Labelframe(content, text="Auditoria de validação", padding=10)
        content.add(inventory_frame, weight=3)
        content.add(audit_frame, weight=2)

        cols = ("name", "category", "rarity", "status")
        self.inventory = ttk.Treeview(inventory_frame, columns=cols, show="headings", height=9)
        for key, title, width in [
            ("name", "Equipamento", 310),
            ("category", "Categoria", 180),
            ("rarity", "Classe", 150),
            ("status", "Propriedade", 150),
        ]:
            self.inventory.heading(key, text=title)
            self.inventory.column(key, width=width, anchor="w")
        self.inventory.pack(fill="both", expand=True)

        audit_cols = ("time", "action", "item", "result", "detail")
        self.audit = ttk.Treeview(audit_frame, columns=audit_cols, show="headings", height=7)
        for key, title, width in [
            ("time", "Horário", 145),
            ("action", "Evento", 170),
            ("item", "Item", 180),
            ("result", "Resultado", 110),
            ("detail", "Detalhe", 340),
        ]:
            self.audit.heading(key, text=title)
            self.audit.column(key, width=width, anchor="w")
        self.audit.pack(fill="both", expand=True)

        footer = ttk.Frame(outer)
        footer.pack(fill="x", pady=(12, 0))
        self.status_var = tk.StringVar(value="Pronto.")
        ttk.Label(footer, textvariable=self.status_var, style="Muted.TLabel").pack(side="left")
        ttk.Button(footer, text="Exportar auditoria CSV", command=self.export_csv).pack(side="right")

    def refresh(self) -> None:
        for tree in (self.inventory, self.audit):
            for row in tree.get_children():
                tree.delete(row)
        items = self.store.list_items()
        self.item_combo["values"] = [item["name"] for item in items]
        if items and self.item_var.get() not in self.item_combo["values"]:
            self.item_var.set(items[0]["name"])
        for item in items:
            self.inventory.insert(
                "", "end",
                values=(item["name"], item["category"], item["rarity"],
                        "Possuído" if item["owned"] else "Bloqueado"),
            )
        for event in self.store.list_events(limit=100):
            self.audit.insert(
                "", "end",
                values=(event["created_at"], event["action"], event["item_name"],
                        event["result"], event["detail"]),
            )
        self.status_var.set(f"{len(items)} itens de demonstração | Banco local SQLite")

    def request_item(self) -> None:
        name = self.item_var.get()
        if not name:
            return
        result, detail = self.store.request_item(name)
        self.status_var.set(detail)
        self.refresh()
        if result == "REJECTED":
            messagebox.showwarning("Solicitação recusada", detail)
        else:
            messagebox.showinfo("Solicitação processada", detail)

    def tamper_request(self) -> None:
        name = self.item_var.get()
        if not name:
            return
        result, detail = self.store.request_item(name, client_claims_owned=True)
        self.status_var.set(detail)
        self.refresh()
        messagebox.showinfo(
            "Teste de validação",
            f"Resultado do servidor simulado: {result}\n\n{detail}",
        )

    def export_csv(self) -> None:
        path = self.store.export_events()
        messagebox.showinfo("Exportação concluída", f"Auditoria exportada para:\n{path}")


def main() -> None:
    root = tk.Tk()
    InventoryLabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
