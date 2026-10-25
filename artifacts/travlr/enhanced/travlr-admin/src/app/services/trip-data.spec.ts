
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing';

import { AuthService } from './auth';
import { TripDataService, Trip } from './trip-data';

describe('TripDataService', () => {
  let service: TripDataService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        {
          provide: AuthService,
          useValue: { getToken: () => 'test-token' }
        }
      ]
    });

    service = TestBed.inject(TripDataService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should retrieve trips from the API', () => {
    service.getTrips().subscribe(trips => {
      expect(trips).toEqual([]);
    });

    const req = httpMock.expectOne(
      'http://localhost:3000/api/trips'
    );

    expect(req.request.method).toBe('GET');
    req.flush([]);
  });

  it('should include an authorization token when adding a trip', () => {
    const trip: Trip = {
      code: 'TEST001',
      name: 'Test Trip',
      length: '3 days',
      start: '2026-11-01',
      resort: 'Test Resort',
      perPerson: '500',
      image: 'test.jpg',
      description: 'Test trip description'
    };

    service.addTrip(trip).subscribe(result => {
      expect(result).toEqual(trip);
    });

    const req = httpMock.expectOne(
      'http://localhost:3000/api/trips'
    );

    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get('Authorization'))
      .toBe('Bearer test-token');

    req.flush(trip);
  });
});
