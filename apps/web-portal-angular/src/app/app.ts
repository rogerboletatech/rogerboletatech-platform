import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatToolbarModule } from '@angular/material/toolbar';
import { finalize } from 'rxjs';
import { BoletaService, PassoBoleta, RespostaBoleta } from './boleta.service';

@Component({
  selector: 'app-root',
  imports: [
    FormsModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatProgressBarModule,
    MatToolbarModule,
  ],
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  private readonly boleta = inject(BoletaService);

  protected readonly pergunta = signal('');
  protected readonly carregando = signal(false);
  protected readonly erro = signal<string | null>(null);
  protected readonly resposta = signal<RespostaBoleta | null>(null);

  protected perguntar(): void {
    const texto = this.pergunta().trim();
    if (!texto || this.carregando()) {
      return;
    }
    this.carregando.set(true);
    this.erro.set(null);
    this.boleta
      .perguntar(texto)
      .pipe(finalize(() => this.carregando.set(false)))
      .subscribe({
        next: (r) => this.resposta.set(r),
        error: () => this.erro.set('O serviço do Boleta não respondeu. Ele está no ar?'),
      });
  }

  protected icone(passo: PassoBoleta): string {
    const d = passo.decision;
    if (d.startsWith('recusado') || d.startsWith('bloqueada')) return 'block';
    if (d === 'fallback') return 'warning';
    return 'check_circle';
  }

  protected classe(passo: PassoBoleta): string {
    const d = passo.decision;
    if (d.startsWith('recusado') || d.startsWith('bloqueada')) return 'bloqueio';
    if (d === 'fallback') return 'alerta';
    return 'ok';
  }
}
