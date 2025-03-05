from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource 
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.boto3sqs import Boto3SQSInstrumentor

from loguru import logger
from app.utils.startup import trace_endpoint, trace_service_name

resource = Resource(attributes={
    "service.name": trace_service_name
})

trace.set_tracer_provider(TracerProvider(resource=resource))
oltp_exporter = OTLPSpanExporter(endpoint=trace_endpoint, insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(oltp_exporter))

tracer = trace.get_tracer(__name__)