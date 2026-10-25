
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Trip, TripDataService } from '../../services/trip-data';

@Component({
  selector: 'app-trip-edit',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './trip-edit.html',
  styleUrl: './trip-edit.css'
})
export class TripEdit implements OnInit {
  trip?: Trip;
  message = 'Loading trip...';
  originalTripCode = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private tripDataService: TripDataService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const code = this.route.snapshot.paramMap.get('code');

    if (!code) {
      this.message = 'No trip code found.';
      this.cdr.detectChanges();
      return;
    }

    this.originalTripCode = code;

    this.tripDataService.getTrip(code).subscribe({
      next: (data: Trip) => {
        console.log('Trip loaded:', data);
        this.trip = data;
        this.message = '';
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('TRIP LOAD ERROR:', err);
        this.message = 'Unable to load trip.';
        this.cdr.detectChanges();
      }
    });
  }

  saveTrip(): void {
    if (!this.trip) {
      this.message = 'No trip to save.';
      this.cdr.detectChanges();
      return;
    }

    this.message = 'Saving changes...';
    this.cdr.detectChanges();

    this.tripDataService.updateTrip(this.originalTripCode, this.trip).subscribe({
      next: (updatedTrip: Trip) => {
        console.log('Trip updated:', updatedTrip);
        this.router.navigate(['']);
      },
      error: (err) => {
        console.error('TRIP UPDATE ERROR:', err);
        this.message = 'Unable to save trip changes.';
        this.cdr.detectChanges();
      }
    });
  }

  deleteTrip(): void {
    if (!this.trip) {
      this.message = 'No trip to delete.';
      this.cdr.detectChanges();
      return;
    }

    const confirmDelete = confirm(`Delete trip "${this.trip.name}"?`);

    if (!confirmDelete) {
      return;
    }

    this.message = 'Deleting trip...';
    this.cdr.detectChanges();

    this.tripDataService.deleteTrip(this.originalTripCode).subscribe({
      next: () => {
        console.log('Trip deleted');
        this.router.navigate(['']);
      },
      error: (err) => {
        console.error('TRIP DELETE ERROR:', err);
        this.message = 'Unable to delete trip.';
        this.cdr.detectChanges();
      }
    });
  }
}
