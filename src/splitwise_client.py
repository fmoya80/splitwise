"""Small client for the initial Splitwise API integration."""

import time
from typing import Any

import requests


class SplitwiseClient:
    """Access a limited set of Splitwise endpoints with an API key."""

    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a GET request and return its decoded JSON response.

        A rate-limited request is retried once after five seconds. Other common
        HTTP errors include an actionable Spanish message for local setup.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        for attempt in range(2):
            response = requests.get(url, headers=self.headers, params=params, timeout=30)

            if response.status_code == 429 and attempt == 0:
                time.sleep(5)
                continue

            error_messages = {
                401: "API Key inválida o ausente.",
                403: "No tiene permisos para acceder a este recurso.",
                404: "Endpoint o recurso no encontrado.",
                429: "Se alcanzó el límite de solicitudes de la API.",
            }
            if response.status_code in error_messages:
                raise requests.HTTPError(
                    error_messages[response.status_code], response=response
                )

            response.raise_for_status()
            return response.json()

        # The loop always returns or raises; this protects static analyzers.
        raise RuntimeError("No se pudo completar la solicitud a Splitwise.")

    def get_current_user(self) -> dict[str, Any]:
        """Return the authenticated Splitwise user."""
        return self._get("/get_current_user")

    def get_groups(self) -> dict[str, Any]:
        """Return groups belonging to the authenticated user."""
        return self._get("/get_groups")

    def get_expenses(
        self,
        dated_after: str | None = None,
        dated_before: str | None = None,
        group_id: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Return one small page of expenses; pagination is intentionally omitted."""
        params = {
            key: value
            for key, value in {
                "dated_after": dated_after,
                "dated_before": dated_before,
                "group_id": group_id,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return self._get("/get_expenses", params=params)
