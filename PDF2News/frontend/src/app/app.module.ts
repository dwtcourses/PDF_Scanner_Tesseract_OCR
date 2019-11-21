import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {
  MatButtonModule,
  MatCheckboxModule,
  MatInputModule,
  MatMenuModule,
  MatSidenavModule,
  MatToolbarModule,
  MatTableModule,
  MatDialogModule,
  MatDatepickerModule,
  MatSelectModule,
  MatCardModule,
  MatFormFieldModule,
  MatGridListModule
} from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StoreModule } from '@ngrx/store';
import { reducers } from './reducers';
import { TopBarComponent } from './top-bar/top-bar.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HomePageComponent } from './home-page/home-page.component';
import { PdfService } from './pdf.service';
import { GraphQLModule } from './graphql.module';
import { UploadPageComponent } from './upload-page/upload-page.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { EditPdfDialogComponent } from './edit-pdf-dialog/edit-pdf-dialog.component';


@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    HomePageComponent,
    UploadPageComponent,
    EditPdfDialogComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MatButtonModule,
    StoreModule.forRoot(reducers),
    BrowserAnimationsModule,
    MatButtonModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatInputModule,
    MatMenuModule,
    MatSidenavModule,
    MatToolbarModule,
    MatTableModule,
    HttpClientModule,
    MatDialogModule,
    MatDatepickerModule,
    MatSelectModule,
    MatCardModule,
    MatGridListModule,
    GraphQLModule,
    MatPaginatorModule
  ],
  providers: [
    PdfService
  ],
  bootstrap: [AppComponent],
  entryComponents: [
    EditPdfDialogComponent
  ]
})
export class AppModule { }
