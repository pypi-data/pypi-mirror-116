import json
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union

import requests
from jwcrypto.jwk import JWK, JWKSet  # type: ignore[import]
from jwcrypto.jws import InvalidJWSSignature  # type: ignore[import]
from jwcrypto.jwt import JWT  # type: ignore[import]

from .auth import BearerAuth
from .client import OAuth2Client
from .token_response import BearerToken
from .utils import validate_url


class IdToken:
    def __init__(self, value: str):
        self.value = value
        self.jwt = JWT(jwt=self.value)
        self.payload: Optional[Dict[str, Any]] = None

    def validate(self, issuer: str, jwks: Dict[str, Any], nonce: Optional[str] = None) -> bool:
        if "keys" in jwks:
            validation_jwks = JWKSet()
            for jwk in jwks.get("keys", []):
                validation_jwks.add(JWK(**jwk))
        else:
            validation_jwks = JWK(**jwks)
        try:
            self.jwt.deserialize(self.value, validation_jwks)
            self.payload = json.loads(self.jwt.claims)
        except InvalidJWSSignature as exc:
            raise ValueError(
                "invalid token signature, or verification key is not matching the signature"
            ) from exc
        issuer_from_token = self.get_claim("iss")
        if not issuer_from_token:
            raise ValueError("no issuer set in this token")
        if issuer != issuer_from_token:
            raise ValueError("unexpected issuer value")
        if nonce:
            nonce_from_token = self.get_claim("nonce")
            if nonce_from_token != nonce:
                raise ValueError(
                    "unexpected nonce value, this token may be intended for a different login transaction",
                    nonce_from_token,
                )
        return True

    @property
    def alg(self) -> str:
        return self.get_header("alg")  # type: ignore

    @property
    def kid(self) -> str:
        return self.get_header("kid")  # type: ignore

    def get_header(self, key: str) -> Any:
        return self.jwt.token.jose_header.get(key)

    def get_claim(self, key: str) -> Any:
        if self.payload:
            return self.payload.get(key)

    def __getattr__(self, item: str) -> Any:
        return self.get_claim(item)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, IdToken):
            return self.value == other.value
        return super().__eq__(other)


class OpenIdConnectTokenResponse(BearerToken):
    def __init__(
        self,
        access_token: str,
        id_token: str,
        expires_in: Optional[int] = None,
        expires_at: Optional[datetime] = None,
        scope: Optional[str] = None,
        refresh_token: Optional[str] = None,
        token_type: str = "Bearer",
        **kwargs: Any,
    ):
        super().__init__(
            access_token=access_token,
            id_token=id_token,
            expires_in=expires_in,
            expires_at=expires_at,
            scope=scope,
            refresh_token=refresh_token,
            token_type=token_type,
            **kwargs,
        )
        self.id_token = IdToken(id_token)


class OpenIdConnectClient(OAuth2Client):
    """
    An OIDC compatible client. It can do everything an OAuth20Client can do, and call the userinfo endpoint.
    """

    token_response_class = OpenIdConnectTokenResponse

    def __init__(
        self,
        *,
        token_endpoint: str,
        jwks_uri: str,
        revocation_endpoint: Optional[str] = None,
        userinfo_endpoint: Optional[str] = None,
        auth: Union[requests.auth.AuthBase, Tuple[str, str], str],
        session: Optional[requests.Session] = None,
    ):
        super().__init__(
            token_endpoint=token_endpoint,
            revocation_endpoint=revocation_endpoint,
            auth=auth,
            session=session,
        )
        self.userinfo_endpoint = userinfo_endpoint
        self.jwks_uri = jwks_uri

    def userinfo(self, access_token: Union[BearerToken, str]) -> Any:
        """
        Calls the userinfo endpoint with the specified access_token and returns the result.
        :param access_token: the access token to use
        :return: the requests Response returned by the userinfo endpoint.
        """
        if not self.userinfo_endpoint:
            raise ValueError("No userinfo endpoint defined for this client")
        return self.session.post(self.userinfo_endpoint, auth=BearerAuth(access_token)).json()

    @classmethod
    def from_discovery_document(
        cls,
        discovery: Dict[str, Any],
        auth: Union[requests.auth.AuthBase, Tuple[str, str], str],
        session: Optional[requests.Session] = None,
        https: bool = True,
    ) -> "OpenIdConnectClient":

        token_endpoint = discovery.get("token_endpoint")
        if token_endpoint is None:
            raise ValueError("token_endpoint not found in that discovery document")
        validate_url(token_endpoint, https=https)
        revocation_endpoint = discovery.get("revocation_endpoint")
        if revocation_endpoint is not None:
            validate_url(revocation_endpoint, https=https)
        userinfo_endpoint = discovery.get("userinfo_endpoint")
        if userinfo_endpoint is not None:
            validate_url(userinfo_endpoint, https=https)
        jwks_uri = discovery.get("jwks_uri")
        if jwks_uri is not None:
            validate_url(userinfo_endpoint, https=https)

        return cls(
            token_endpoint=token_endpoint,
            revocation_endpoint=revocation_endpoint,
            userinfo_endpoint=userinfo_endpoint,
            jwks_uri=jwks_uri,
            auth=auth,
            session=session,
        )
