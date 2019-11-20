import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditPdfDialogComponent } from './edit-pdf-dialog.component';

describe('EditPdfDialogComponent', () => {
  let component: EditPdfDialogComponent;
  let fixture: ComponentFixture<EditPdfDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditPdfDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditPdfDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
