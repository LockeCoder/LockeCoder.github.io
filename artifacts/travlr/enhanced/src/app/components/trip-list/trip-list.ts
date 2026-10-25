import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TripCard } from '../trip-card/trip-card';
import { Trip, TripDataService } from '../../services/trip-data';

@Component({
  selector: 'app-trip-list',
  standalone: true,
  imports: [CommonModule, RouterLink, TripCard],
  templateUrl: './trip-list.html',
  styleUrl: './trip-list.css'
})
export class TripList implements OnInit {
  trips: Trip[] = [];
  message = 'Loading trips...';

  constructor(
    private tripDataService: TripDataService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.message = 'Loading trips...';

    this.tripDataService.getTrips().subscribe({
      next: (data: Trip[]) => {
        console.log('Trips received:', data);
        this.trips = data;
        this.message = this.trips.length ? '' : 'No trips found.';
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('API ERROR:', err);
        this.message = 'Unable to load trips.';
        this.cdr.detectChanges();
      }
    });
  }
}