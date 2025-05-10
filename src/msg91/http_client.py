"""
HTTP Client for MSG91 API
"""

from typing import Any, Dict, Optional, cast
from urllib.parse import urljoin

import httpx

from msg91.exceptions import APIError, AuthenticationError, MSG91Exception, ValidationError


class HTTPClient:
    """
    HTTP client for making requests to the MSG91 API

    https://docs.msg91.com/sms
    """

    BASE_URL = "https://control.msg91.com/api/v5"

    def __init__(
        self,
        auth_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        **httpx_kwargs: Any,
    ):
        self.auth_key = auth_key
        self.base_url = base_url or self.BASE_URL
        self.httpx_kwargs = httpx_kwargs
        self.timeout = timeout
        self.client = httpx.Client(timeout=self.timeout, **self.httpx_kwargs)

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a request to the MSG91 API"""
        url = urljoin(self.base_url, path)

        # Prepare headers
        request_headers = {
            "Content-Type": "application/json",
            "authkey": self.auth_key,
        }

        if headers:
            request_headers.update(headers)

        try:
            response = self.client.request(
                method,
                url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
            )

            response_data = self._parse_response(response)
            return response_data

        except httpx.RequestError as e:
            raise MSG91Exception(f"Network error: {str(e)}") from e

    def _parse_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Parse the API response and handle errors"""
        try:
            data = response.json()
        except ValueError:
            data = {"raw_content": response.text}

        if not response.is_success:
            # Handle error responses
            error_type = data.get("type", "").lower() if isinstance(data, dict) else ""
            message = (
                data.get("message", "Unknown error") if isinstance(data, dict) else "Unknown error"
            )

            if response.status_code == 401:
                raise AuthenticationError(
                    message=message,
                    status=response.status_code,
                    details=data,
                )
            elif response.status_code == 400 or error_type == "validation":
                raise ValidationError(
                    message=message,
                    status=response.status_code,
                    details=data,
                )
            else:
                raise APIError(
                    message=message,
                    status=response.status_code,
                    details=data,
                )

        return cast(Dict[str, Any], data)

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a GET request"""
        return self.request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request"""
        return self.request(
            "POST", path, params=params, data=data, json_data=json_data, headers=headers
        )

    def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request"""
        return self.request(
            "PUT", path, params=params, data=data, json_data=json_data, headers=headers
        )

    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self.request("DELETE", path, params=params, headers=headers)
