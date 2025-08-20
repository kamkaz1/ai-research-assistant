import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ResearchResult {
  title: string;
  summary: string;
  key_points: string[];
  sources: Array<{title: string; url: string}>;
}

interface ResearchHistory {
  id: number;
  query: string;
  result: ResearchResult;
  created_at: string;
  status: string;
}

interface ApiResponse {
  query: string;
  timestamp: string;
  result: ResearchResult;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class AppComponent implements OnInit {
  title = 'AI Research Assistant';
  query: string = '';
  researchResult: ResearchResult | null = null;
  loading: boolean = false;
  error: string | null = null;
  researchHistory: ResearchHistory[] = [];
  showHistory: boolean = false;
  stats: any = null;

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.loadStats();
  }

  performResearch() {
    if (!this.query.trim()) {
      this.error = "Please enter a research query.";
      return;
    }

    this.loading = true;
    this.error = null;
    this.researchResult = null;

    const encodedQuery = encodeURIComponent(this.query.trim());
    
    this.http.get<ApiResponse>(`${environment.backendUrl}/research?query=${encodedQuery}`)
      .subscribe({
        next: (response) => {
          this.researchResult = response.result;
          this.loading = false;
          this.loadHistory(); // Refresh history after new research
        },
        error: (err) => {
          console.error('API Error:', err);
          this.error = err.error?.error || err.error?.details || 'Failed to fetch research results. Please try again.';
          this.loading = false;
        }
      });
  }

  loadHistory() {
    this.http.get<{history: ResearchHistory[], count: number}>(`${environment.backendUrl}/history?limit=10`)
      .subscribe({
        next: (response) => {
          this.researchHistory = response.history;
        },
        error: (err) => {
          console.error('Failed to load history:', err);
        }
      });
  }

  loadStats() {
    this.http.get<any>(`${environment.backendUrl}/stats`)
      .subscribe({
        next: (response) => {
          this.stats = response;
        },
        error: (err) => {
          console.error('Failed to load stats:', err);
        }
      });
  }

  toggleHistory() {
    this.showHistory = !this.showHistory;
    if (this.showHistory) {
      this.loadHistory();
    }
  }

  loadFromHistory(historyItem: ResearchHistory) {
    this.query = historyItem.query;
    this.researchResult = historyItem.result;
    this.error = null;
    this.showHistory = false;
  }

  clearResults() {
    this.researchResult = null;
    this.error = null;
    this.query = '';
  }

  openSource(url: string) {
    console.log('Opening source URL:', url);
    
    // Validate URL
    if (!url || url.trim() === '') {
      console.error('Empty URL provided');
      return;
    }
    
    // Ensure URL has proper protocol
    let finalUrl = url.trim();
    if (!finalUrl.startsWith('http://') && !finalUrl.startsWith('https://')) {
      finalUrl = 'https://' + finalUrl;
    }
    
    console.log('Final URL:', finalUrl);
    
    try {
      window.open(finalUrl, '_blank', 'noopener,noreferrer');
    } catch (error) {
      console.error('Error opening URL:', error);
      // Fallback: try to open without noopener
      window.open(finalUrl, '_blank');
    }
  }

  copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).then(() => {
      // Could add a toast notification here
      console.log('Copied to clipboard');
    });
  }

  getStatusColor(status: string): string {
    return status === 'success' ? 'text-success' : 'text-danger';
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleString();
  }

  getFullResearchText(): string {
    if (!this.researchResult) return '';
    
    let text = `${this.researchResult.title}\n\n`;
    text += `SUMMARY:\n${this.researchResult.summary}\n\n`;
    
    if (this.researchResult.key_points.length > 0) {
      text += `KEY POINTS:\n`;
      this.researchResult.key_points.forEach((point, index) => {
        text += `${index + 1}. ${point}\n`;
      });
      text += '\n';
    }
    
    if (this.researchResult.sources.length > 0) {
      text += `SOURCES:\n`;
      this.researchResult.sources.forEach((source, index) => {
        text += `${index + 1}. ${source.title} (${source.url})\n`;
      });
    }
    
    return text;
  }

  downloadAsText() {
    const text = this.getFullResearchText();
    const blob = new Blob([text], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }
}
