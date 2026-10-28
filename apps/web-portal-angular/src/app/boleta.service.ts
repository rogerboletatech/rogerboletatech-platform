import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

// Formato do contrato AsyncAPI (libs/contracts-specs/asyncapi/console-glass-box.yaml).
export interface PassoBoleta {
  interacaoId: string;
  ordem: number;
  step: string;
  decision: string;
  detalhe: string;
  traceId: string;
  emitidoEm: string;
}

export interface RespostaFinalBoleta {
  interacaoId: string;
  resposta: string;
  autor: string;
  fallback: boolean;
  bloqueada: boolean;
}

export type EventoBoleta =
  | { evento: 'passo'; dados: PassoBoleta }
  | { evento: 'resposta'; dados: RespostaFinalBoleta };

// Lê um bloco SSE ("event: ...\ndata: ...") e devolve o evento tipado, ou null se não for um evento válido.
export function lerBlocoSse(bloco: string): EventoBoleta | null {
  let nome = '';
  let dados = '';
  for (const linha of bloco.split('\n')) {
    if (linha.startsWith('event: ')) nome = linha.slice(7);
    if (linha.startsWith('data: ')) dados += linha.slice(6);
  }
  if (!dados) return null;
  const payload = JSON.parse(dados);
  if (nome === 'passo') return { evento: 'passo', dados: payload };
  if (nome === 'resposta') return { evento: 'resposta', dados: payload };
  return null;
}

@Injectable({ providedIn: 'root' })
export class BoletaService {
  private readonly http = inject(HttpClient);

  perguntarStream(pergunta: string): Observable<EventoBoleta> {
    return new Observable<EventoBoleta>((observador) => {
      const controle = new AbortController();
      fetch('/boleta/perguntar/stream', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ pergunta }),
        signal: controle.signal,
      })
        .then(async (resposta) => {
          if (!resposta.ok || !resposta.body) {
            throw new Error(`HTTP ${resposta.status}`);
          }
          const leitor = resposta.body.pipeThrough(new TextDecoderStream()).getReader();
          let pendente = '';
          for (;;) {
            const { value, done } = await leitor.read();
            if (done) break;
            pendente += value;
            const blocos = pendente.split('\n\n');
            pendente = blocos.pop() ?? '';
            for (const bloco of blocos) {
              const evento = lerBlocoSse(bloco);
              if (evento) observador.next(evento);
            }
          }
          observador.complete();
        })
        .catch((erro) => {
          if (!controle.signal.aborted) observador.error(erro);
        });
      return () => controle.abort();
    });
  }
}
