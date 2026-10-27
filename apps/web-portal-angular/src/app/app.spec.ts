import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { App } from './app';
import { RespostaBoleta } from './boleta.service';

const respostaFake: RespostaBoleta = {
  resposta: 'Use ShedLock.',
  autor: 'Boleta (agente de IA)',
  fallback: false,
  bloqueada: false,
  passos: [
    { step: 'guarda_entrada', decision: 'permitido', detalhe: '' },
    { step: 'responder', decision: 'llm', detalhe: '' },
  ],
};

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
  });

  it('renderiza o título do console', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('h1')?.textContent).toContain('Console Glass-Box');
  });

  it('não envia pergunta vazia', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.componentInstance['perguntar']();
    http.expectNone('/boleta/perguntar');
  });

  it('mostra a resposta e os passos devolvidos pelo Boleta', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.componentInstance['pergunta'].set('meu @Scheduled roda em 4 pods');
    fixture.componentInstance['perguntar']();

    http.expectOne('/boleta/perguntar').flush(respostaFake);
    fixture.detectChanges();

    const texto = fixture.nativeElement.textContent as string;
    expect(texto).toContain('Use ShedLock.');
    expect(texto).toContain('guarda_entrada');
    expect(fixture.nativeElement.querySelectorAll('.passos li').length).toBe(2);
  });

  it('mostra erro quando o serviço cai', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.componentInstance['pergunta'].set('oi');
    fixture.componentInstance['perguntar']();

    http.expectOne('/boleta/perguntar').flush('', { status: 503, statusText: 'Unavailable' });
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('[role="alert"]')?.textContent).toContain('não respondeu');
  });
});
