
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { TripEdit } from './trip-edit';
import { Trip, TripDataService } from '../../services/trip-data';

describe('TripEdit', () => {
  const sampleTrip: Trip = {
    code: 'TEST001',
    name: 'Test Trip',
    length: '3 days',
    start: '2026-11-01',
    resort: 'Test Resort',
    perPerson: '500',
    image: 'test.jpg',
    description: 'Test trip description'
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TripEdit],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: convertToParamMap({ code: 'TEST001' })
            }
          }
        },
        {
          provide: TripDataService,
          useValue: {
            getTrip: (_code: string) => of(sampleTrip)
          }
        }
      ]
    }).compileComponents();
  });

  it('should load the requested trip for editing', async () => {
    const fixture = TestBed.createComponent(TripEdit);
    fixture.detectChanges();
    await fixture.whenStable();

    expect(fixture.componentInstance.originalTripCode).toBe('TEST001');
    expect(fixture.componentInstance.trip?.name).toBe('Test Trip');
  });
});
