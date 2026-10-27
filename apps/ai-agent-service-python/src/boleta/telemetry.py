"""Spans OpenTelemetry do Boleta: a caixa de vidro (ficha técnica, princípio 2).

Atributos padronizados: boleta.step, boleta.tool, boleta.decision.
O exporter (OTLP para o Grafana, Módulo 7) é configurado na borda, não aqui.
"""

from contextlib import contextmanager

from opentelemetry import trace

tracer = trace.get_tracer("boleta")


@contextmanager
def passo(nome: str, **atributos: str):
    with tracer.start_as_current_span(f"boleta.{nome}") as span:
        span.set_attribute("boleta.step", nome)
        for chave, valor in atributos.items():
            span.set_attribute(f"boleta.{chave}", valor)
        yield span
