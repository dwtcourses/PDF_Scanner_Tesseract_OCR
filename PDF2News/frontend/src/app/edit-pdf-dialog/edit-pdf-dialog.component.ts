import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { PdfService } from '../pdf.service';
import { environment } from 'src/environments/environment';
import { Store, select } from '@ngrx/store';
import { SET_PDFS } from '../reducers/pdfs-reducer'
import { NgForm } from '@angular/forms';


@Component({
  selector: 'app-edit-pdf-dialog',
  templateUrl: './edit-pdf-dialog.component.html',
  styleUrls: ['./edit-pdf-dialog.component.scss']
})
export class EditPdfDialogComponent implements OnInit {
  @ViewChild('pdfUpload', null) pdfUpload: any;
  pdfArrayData: any[] = [];

  constructor(
    public dialogRef: MatDialogRef<EditPdfDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public pdfData: any,
    private pdfService: PdfService,
    private store: Store<any>
  ) { 
    store.pipe(select('pdfs'))
    .subscribe(pdfs => {
      this.pdfArrayData = pdfs;
    })
  }

  ngOnInit() {
  }

  clickUpload(){
    this.pdfUpload.nativeElement.click();
  }

  handleFileInput(files){
    console.log(files);
    this.pdfData.file = files[0];
  }

  save(uploadForm: NgForm){
    if (uploadForm.invalid || !this.pdfData.file){return;}

    const {
        id,
        file,
        description,
        tags
      } = this.pdfData;

      this.pdfService.editPdf(id, file, description, tags)
      .subscribe(es => {
        this.getPdfs();
      })
  }

  getPdfs(){
    this.pdfService.getPdfs()
    .subscribe(res => {
      const pdfArrayData = (res as
        any).data.getPdfs.pdfs.map(p => {
          const {id, description, tags} = p;
          const pathParts = p.fileLocation.split('/');
          const pdfPath = pathParts[pathParts.length - 1];
          
          return{
            id,
            description,
            tags,
            pdfUrl: `${environment.pdfsUrl}/${pdfPath}`
          }
        });

        this.store.dispatch({
          type: SET_PDFS,
          payload: pdfArrayData
        });

        this.dialogRef.close()
    })
  }
}

