
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { TripCard } from './trip-card';
import { Trip } from '../../services/trip-data';

describe('TripCard', () => {
  let component: TripCard;
  let fixture: ComponentFixture<TripCard>;

  const mockTrip: Trip = {
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
      imports: [TripCard],
      providers: [provideRouter([])]
    }).compileComponents();

    fixture = TestBed.createComponent(TripCard);
    component = fixture.componentInstance;

    fixture.componentRef.setInput('trip', mockTrip);
    fixture.detectChanges();

    await fixture.whenStable();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should display the trip information', () => {
    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.textContent).toContain('Test Trip');
    expect(compiled.textContent).toContain('TEST001');
    expect(compiled.textContent).toContain('Test Resort');
  });
});
