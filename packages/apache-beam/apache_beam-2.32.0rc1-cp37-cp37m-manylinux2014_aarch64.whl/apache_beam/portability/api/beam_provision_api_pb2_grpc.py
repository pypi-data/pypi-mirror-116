# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
from __future__ import absolute_import
from builtins import object
import grpc

from . import beam_provision_api_pb2 as beam__provision__api__pb2


class ProvisionServiceStub(object):
    """A service to provide runtime provisioning information to the SDK harness
    worker instances -- such as pipeline options, resource constraints and
    other job metadata -- needed by an SDK harness instance to initialize.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProvisionInfo = channel.unary_unary(
                '/org.apache.beam.model.fn_execution.v1.ProvisionService/GetProvisionInfo',
                request_serializer=beam__provision__api__pb2.GetProvisionInfoRequest.SerializeToString,
                response_deserializer=beam__provision__api__pb2.GetProvisionInfoResponse.FromString,
                )


class ProvisionServiceServicer(object):
    """A service to provide runtime provisioning information to the SDK harness
    worker instances -- such as pipeline options, resource constraints and
    other job metadata -- needed by an SDK harness instance to initialize.
    """

    def GetProvisionInfo(self, request, context):
        """Get provision information for the SDK harness worker instance.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProvisionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProvisionInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProvisionInfo,
                    request_deserializer=beam__provision__api__pb2.GetProvisionInfoRequest.FromString,
                    response_serializer=beam__provision__api__pb2.GetProvisionInfoResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'org.apache.beam.model.fn_execution.v1.ProvisionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ProvisionService(object):
    """A service to provide runtime provisioning information to the SDK harness
    worker instances -- such as pipeline options, resource constraints and
    other job metadata -- needed by an SDK harness instance to initialize.
    """

    @staticmethod
    def GetProvisionInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.apache.beam.model.fn_execution.v1.ProvisionService/GetProvisionInfo',
            beam__provision__api__pb2.GetProvisionInfoRequest.SerializeToString,
            beam__provision__api__pb2.GetProvisionInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
