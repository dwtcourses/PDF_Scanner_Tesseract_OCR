import { Component, OnInit } from '@angular/core';
import { PdfService } from '../pdf.service';
import { environment } from 'src/environments/environment';
import { NgForm } from '@angular/forms'; 

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent implements OnInit {
  pdfUrls: string[] = [];
  query: any = <any>{};

  constructor(
    private pdfService: PdfService
  ) { }

  ngOnInit() {
    this.getPdfs();
  }

  getPdfs(){
    this.pdfService.getPdfs()
    .subscribe(res => {
      this.pdfUrls = (res as any).data.getPdfs.pdfs.map(p =>
        {
          const pathParts = p.fileLocation.split('/');
          const pdfPath = pathParts[pathParts.length - 1];
          
          return `${environment.pdfsUrl}/${pdfPath}`;
        });
      })
  }

  searchPdfs(searchForm: NgForm){
    if (searchForm.invalid){ return; }

    this.searchPdfsQuery();
  }

  searchPdfsQuery(){
    this.pdfService.searchPdfs(this.query.search)
    .subscribe(res => {
      this.pdfUrls = (res as any)
      .data.searchPdfs.pdfs.map(p => {
        const pathParts = p.fileLocation.split('/');
        const pdfPath = pathParts[pathParts.length - 1];

        return `${environment.pdfsUrl}/${pdfPath}`;
      });
    })
  }
}
