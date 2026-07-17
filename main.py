"""Validate a local Splitwise connection and save initial raw API responses."""

import argparse

from src.config import BASE_URL, SPLITWISE_API_KEY
from src.splitwise_client import SplitwiseClient
from src.utils import ensure_directories, save_json


def parse_arguments() -> argparse.Namespace:
    """Parse optional filters for the sample expenses request."""
    parser = argparse.ArgumentParser(description="Extrae una muestra de datos de Splitwise.")
    parser.add_argument("--dated-after", help="Fecha ISO 8601 inclusiva de inicio.")
    parser.add_argument("--dated-before", help="Fecha ISO 8601 inclusiva de fin.")
    group_selection = parser.add_mutually_exclusive_group()
    group_selection.add_argument("--group-id", type=int, help="Identificador del grupo a consultar.")
    group_selection.add_argument(
        "--select-group",
        action="store_true",
        help="Muestra un menú para elegir interactivamente el grupo a consultar.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Cantidad de gastos de prueba (10 por defecto).")
    return parser.parse_args()


def main() -> None:
    """Fetch and persist the current user, groups, and a sample of expenses."""
    args = parse_arguments()
    ensure_directories()
    client = SplitwiseClient(SPLITWISE_API_KEY, BASE_URL)

    current_user = client.get_current_user()
    save_json(current_user, "data/raw/current_user.json")
    user = current_user.get("user", current_user)
    print("Usuario conectado:")
    print(f"  Nombre: {user.get('first_name', '')} {user.get('last_name', '')}".strip())
    print(f"  User ID: {user.get('id', 'No disponible')}")
    print(f"  Email: {user.get('email', 'No disponible')}")

    groups_response = client.get_groups()
    save_json(groups_response, "data/raw/groups.json")
    groups = groups_response.get("groups", [])
    print(f"\\nGrupos encontrados: {len(groups)}")
    for index, group in enumerate(groups, start=1):
        print(
            f"  {index}. Nombre: {group.get('name', 'Sin nombre')} | "
            f"ID: {group.get('id', 'No disponible')} | "
            f"Tipo: {group.get('group_type', 'No disponible')}"
        )

    group_id = args.group_id
    if args.select_group:
        group_id = select_group(groups)

    expenses_response = client.get_expenses(
        dated_after=args.dated_after,
        dated_before=args.dated_before,
        group_id=group_id,
        limit=args.limit,
    )
    save_json(expenses_response, "data/raw/sample_expenses.json")
    expenses = expenses_response.get("expenses", [])
    print(f"\\nGastos de prueba extraídos: {len(expenses)}")


def select_group(groups: list[dict]) -> int:
    """Prompt for a numbered group from the groups returned by Splitwise."""
    if not groups:
        raise RuntimeError("No hay grupos disponibles para seleccionar.")

    while True:
        choice = input("\\nSeleccione el número del grupo que desea extraer: ").strip()
        try:
            selected_group = groups[int(choice) - 1]
            group_id = selected_group["id"]
        except (ValueError, IndexError, KeyError):
            print("Selección no válida. Ingrese uno de los números mostrados.")
            continue

        print(f"Grupo seleccionado: {selected_group.get('name', 'Sin nombre')} (ID: {group_id})")
        return int(group_id)


if __name__ == "__main__":
    main()
