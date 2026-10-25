import { ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Trip, TripDataService } from '../../services/trip-data';

@Component({
  selector: 'app-trip-add',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './trip-add.html',
  styleUrl: './trip-add.css'
})
export class TripAdd {
  trip: Trip = {
    code: '',
    name: '',
    length: '',
    start: '',
    resort: '',
    perPerson: '',
    image: '',
    description: ''
  };

  message = '';

  constructor(
    private router: Router,
    private tripDataService: TripDataService,
    private cdr: ChangeDetectorRef
  ) {}

  saveNewTrip(): void {
    this.message = 'Saving new trip...';
    this.cdr.detectChanges();

    this.tripDataService.addTrip(this.trip).subscribe({
      next: (newTrip: Trip) => {
        console.log('Trip added:', newTrip);
        this.router.navigate(['']);
      },
      error: (err) => {
        console.error('ADD TRIP ERROR:', err);
        this.message = 'Unable to add trip.';
        this.cdr.detectChanges();
      }
    });
  }
}