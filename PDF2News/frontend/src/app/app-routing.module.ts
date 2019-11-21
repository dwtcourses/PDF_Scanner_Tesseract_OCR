import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomePageComponent } from './home-page/home-page.component';
import { UploadPageComponent } from './upload-page/upload-page.component';

const routes: Routes = [
  {path: '', component: HomePageComponent},
  {path: 'upload', component: UploadPageComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
