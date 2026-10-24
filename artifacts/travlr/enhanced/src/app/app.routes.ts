import { Routes } from '@angular/router';
import { TripList } from './components/trip-list/trip-list';
import { TripEdit } from './components/trip-edit/trip-edit';
import { TripAdd } from './components/trip-add/trip-add';
import { Login } from './components/login/login';
import { authGuard } from './auth.guard';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: '', component: TripList, canActivate: [authGuard] },
  { path: 'add', component: TripAdd, canActivate: [authGuard] },
  { path: 'edit/:code', component: TripEdit, canActivate: [authGuard] }
];