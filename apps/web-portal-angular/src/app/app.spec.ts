import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { App } from './app';
import { BoletaService, EventoBoleta, lerBlocoSse } from './boleta.service';

const passoBase = {
  interacaoId: '01JEXAMPLE0000000000000000',
  traceId: '4bf92f3577b34da6a3ce929d0e0e4736',
  emitidoEm: '2026-10-27T10:00:00Z',
  detalhe: '',
};

class BoletaFalso {
  readonly fluxo = new Subject<EventoBoleta>();
  chamadas = 0;

  perguntarStream() {
    this.chamadas++;
    return this.fluxo.asObservable();
  }
}

describe('lerBlocoSse', () => {
  it('lê um evento de passo do formato SSE', () => {
    const bloco = 'event: passo\ndata: {"ordem":1,"step":"guarda_entrada","decision":"permitido"}';
    expect(lerBlocoSse(bloco)).toEqual({
      evento: 'passo',
      dados: { ordem: 1, step: 'guarda_entrada', decision: 'permitido' },
    });
  });

  it('ignora bloco sem dados', () => {
    expect(lerBlocoSse('event: passo')).toBeNull();
  });
});

describe('App', () => {
  let falso: BoletaFalso;

  beforeEach(async () => {
    falso = new BoletaFalso();
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [{ provide: BoletaService, useValue: falso }],
    }).compileComponents();
  });

  it('renderiza o título do console', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('.titulo')?.textContent).toContain('Console Glass-Box');
  });

  it('não envia pergunta vazia', () => {
    const fixture = TestBed.createComponent(App);
    fixture.componentInstance['perguntar']();
    expect(falso.chamadas).toBe(0);
  });

  it('mostra cada passo assim que chega, antes da resposta final', () => {
    const fixture = TestBed.createComponent(App);
    fixture.componentInstance['pergunta'].set('meu @Scheduled roda em 4 pods');
    fixture.componentInstance['perguntar']();

    falso.fluxo.next({ evento: 'passo', dados: { ...passoBase, ordem: 1, step: 'guarda_entrada', decision: 'permitido' } });
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelectorAll('mat-list-item').length).toBe(1);
    expect(fixture.nativeElement.textContent).not.toContain('Use ShedLock.');

    falso.fluxo.next({ evento: 'passo', dados: { ...passoBase, ordem: 2, step: 'busca_diretrizes', decision: '#01' } });
    falso.fluxo.next({
      evento: 'resposta',
      dados: { interacaoId: passoBase.interacaoId, resposta: 'Use ShedLock.', autor: 'Boleta (agente de IA)', fallback: false, bloqueada: false },
    });
    fixture.detectChanges();

    const texto = fixture.nativeElement.textContent as string;
    expect(fixture.nativeElement.querySelectorAll('mat-list-item').length).toBe(2);
    expect(texto).toContain('Use ShedLock.');
    expect(texto).toContain('busca_diretrizes');
  });

  it('mostra erro quando o stream falha', () => {
    const fixture = TestBed.createComponent(App);
    fixture.componentInstance['pergunta'].set('oi');
    fixture.componentInstance['perguntar']();

    falso.fluxo.error(new Error('HTTP 503'));
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('[role="alert"]')?.textContent).toContain('não respondeu');
  });
});
