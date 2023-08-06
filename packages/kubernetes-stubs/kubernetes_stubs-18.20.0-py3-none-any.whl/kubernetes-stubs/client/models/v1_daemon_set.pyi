import datetime
import typing

import kubernetes.client

class V1DaemonSet:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1DaemonSetSpec]
    status: typing.Optional[kubernetes.client.V1DaemonSetStatus]
    def __init__(
        self,
        *,
        api_version: typing.Optional[str] = ...,
        kind: typing.Optional[str] = ...,
        metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ...,
        spec: typing.Optional[kubernetes.client.V1DaemonSetSpec] = ...,
        status: typing.Optional[kubernetes.client.V1DaemonSetStatus] = ...
    ) -> None: ...
