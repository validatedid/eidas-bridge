"""
DID Document Service classes.

Copyright 2017-2019 Government of Canada
Public Services and Procurement Canada - buyandsell.gc.ca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

class Service:
    """
    Service specification to embed in DID document.

    Retains DIDs as raw values (orientated toward indy-facing operations),
    everything else as URIs (oriented toward W3C-facing operations).
    """

    def __init__(
        self,
        did: str,
        ident: str,
        typ: str,
        endpoint: str,
    ):
        """
        Initialize the Service instance.

        Retain service specification particulars.

        Args:
            did: DID of DID document embedding service, specified raw
                (operation converts to URI)
            ident: identifier for service
            typ: service type
            endpoint: service endpoint

        Raises:
            ValueError: on bad input controller DID

        """

        self._did = did
        self._id = ident
        self._type = typ
        self._endpoint = endpoint

    @property
    def did(self) -> str:
        """Accessor for the DID value."""

        return self._did

    @property
    def id(self) -> str:
        """Accessor for the service identifier."""

        return self._id

    @property
    def type(self) -> str:
        """Accessor for the service type."""

        return self._type

    @property
    def endpoint(self) -> str:
        """Accessor for the endpoint value."""

        return self._endpoint

    def to_dict(self) -> dict:
        """Return dict representation of service to embed in DID document."""

        return {
            "id": self.id, 
            "type": self.type, 
            "serviceEndpoint": self.endpoint
        }
