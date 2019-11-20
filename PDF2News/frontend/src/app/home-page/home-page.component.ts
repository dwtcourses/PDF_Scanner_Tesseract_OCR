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

  constructor() { }

  ngOnInit() {
  }

}
