import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface PassoBoleta {
  step: string;
  decision: string;
  detalhe: string;
}

export interface RespostaBoleta {
  resposta: string;
  autor: string;
  fallback: boolean;
  bloqueada: boolean;
  passos: PassoBoleta[];
}

@Injectable({ providedIn: 'root' })
export class BoletaService {
  private readonly http = inject(HttpClient);

  perguntar(pergunta: string): Observable<RespostaBoleta> {
    return this.http.post<RespostaBoleta>('/boleta/perguntar', { pergunta });
  }
}
