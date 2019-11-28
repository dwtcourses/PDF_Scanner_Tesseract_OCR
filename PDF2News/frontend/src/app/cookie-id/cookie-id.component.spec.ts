import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CookieIdComponent } from './cookie-id.component';

describe('CookieIdComponent', () => {
  let component: CookieIdComponent;
  let fixture: ComponentFixture<CookieIdComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CookieIdComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CookieIdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
