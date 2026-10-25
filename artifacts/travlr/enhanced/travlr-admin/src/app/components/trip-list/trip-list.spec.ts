
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { TripList } from './trip-list';
import { TripDataService } from '../../services/trip-data';

describe('TripList', () => {
  let component: TripList;
  let fixture: ComponentFixture<TripList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TripList],
      providers: [
        provideRouter([]),
        {
          provide: TripDataService,
          useValue: {
            getTrips: () => of([])
          }
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(TripList);
    component = fixture.componentInstance;

    fixture.detectChanges();
    await fixture.whenStable();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should display a message when no trips are returned', () => {
    expect(component.trips).toEqual([]);

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('No trips found.');
  });
});
