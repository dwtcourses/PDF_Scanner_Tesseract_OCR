import { Component, OnInit, ViewChild } from '@angular/core';
import { PdfService } from '../pdf.service';
import { environment } from 'src/environments/environment';
import { MatDialog } from '@angular/material';
import { EditPdfDialogComponent } from '../edit-pdf-dialog/edit-pdf-dialog.component';
import { Store, select } from '@ngrx/store';
import { SET_PDFS } from '../reducers/pdfs-reducer';
import { NgForm } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { CookieIdComponent } from '../cookie-id/cookie-id.component';

@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {
  cookieVal: string;
  pdfData: any = <any>{};
  pdfArrayData: any[] = [];
  page: number = 1;
  totalPdfs: number = 0;
  
  @ViewChild('pdfUpload', null) pdfUpload: any;
  displayedColumns: string[] = [
    'pdfUrl',
    'description',
    'tags',
    'edit',
    'delete'
  ]

  constructor(
    public cookieService: CookieService,
    private pdfService: PdfService,
    public dialog: MatDialog,
    private store: Store<any>,
  ) {
    store.pipe(select('pdfs'))
      .subscribe(pdfs => {
        this.pdfArrayData = pdfs;
      })
  }

  ngOnInit() {
    this.getPdfs();
    this.cookieService.set('Cookie Name', 'Cookie Value');
    this.cookieVal = this.cookieService.get('Cookie Name');
  }

  clickUpload() {
    this.pdfUpload.nativeElement.click();
  }

  handleFileInput(files) {
    console.log(files);
    this.pdfData.file = files[0];
  }

  save(uploadForm: NgForm) {
    if (uploadForm.invalid || !this.pdfData.file) { return; }
    
    const {
      file,
      description,
      tags
    } = this.pdfData;

    this.pdfService.addPdf(file, description, tags)
      .subscribe(res => {
        this.getPdfs();
      })
  }

  getPdfs() {
    this.pdfService.getPdfs(this.page)
      .subscribe(res => {
        const pdfArrayData = (res as any).data.getPdfs.pdfs.map(p => {
          
          const { 
            id, 
            description, 
            tags } = p;

          const pathParts = p.fileLocation.split('/');
          const pdfPath = pathParts[pathParts.length - 1];
          return {
            id,
            description,
            tags,
            pdfUrl: `${environment.pdfsUrl}/${pdfPath}`
          }
        });
        this.page = (res as any).data.getPdfs.page;
        this.totalPdfs = (res as any).data.getPdfs.totalPdfs;
        this.store.dispatch({ type: SET_PDFS, payload: pdfArrayData });
      })
  }

  openEditDialog(index: number) {
    const dialogRef = this.dialog.open(EditPdfDialogComponent, {
      width: '70vw',
      data: this.pdfArrayData[index] || {}
    })

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

  deletePdf(index: number) {
    const { id } = this.pdfArrayData[index];
    this.pdfService.deletePdf(id)
      .subscribe(res => {
        this.getPdfs();
      })
  }

  myCookie = new CookieIdComponent('hello');
}
