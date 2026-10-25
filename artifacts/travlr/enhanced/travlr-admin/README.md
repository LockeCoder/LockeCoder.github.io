# TravlrAdmin

TravlrAdmin is the Angular administrator single-page application (SPA) for the CS 465 Travlr Getaways full stack project. This application provides the administrative interface used to manage trip data through the separate Travlr Getaways backend API.

The admin application was built with Angular and tested against an Express, Node.js, MongoDB, and Mongoose backend. It supports authenticated administrator workflows including login, trip retrieval, adding trips, editing trips, updating trips, and deleting trips.

## Overview

This project demonstrates front-end single-page application development using Angular. The application connects to a separate backend REST API to retrieve and manage trip records. Administrative actions are protected through JWT-based authentication, with bearer tokens used when making secured API requests.

The customer-facing website and backend API are maintained separately in the `travlr-express` project folder, while this repository contains the Angular administrator interface.

## What This Repository Contains

- Angular administrator SPA
- Login interface for administrator authentication
- Trip list view
- Add trip functionality
- Edit/update trip functionality
- Delete trip functionality
- Angular routing for admin navigation
- Auth guard protection for restricted routes
- Service-based API communication
- JWT bearer token handling for protected API requests

## Related Project Structure

In the larger local CS-465 project folder, the application was organized as two separate project folders:

- `travlr-express` — backend, customer-facing site, REST API, MongoDB integration, and authentication
- `travlr-admin` — Angular administrator SPA used to manage trip data through the backend API

This repository contains the **Angular admin application**. The backend API must be running separately for the admin application to retrieve and manage trip data.

## Tech Stack

- Angular
- TypeScript
- HTML
- CSS
- Angular Router
- Angular Forms
- REST API integration
- JSON Web Token authentication
- Node.js / Express backend connection
- MongoDB / Mongoose backend connection

## Core Features

### Administrator Login

The admin application includes a login workflow that authenticates an administrator against the backend API. After successful authentication, the returned JWT token is used to access protected administrative endpoints.

### Trip List

The trip list view retrieves trip data from the backend API and displays available trips in the Angular admin interface.

### Add Trip

Administrators can add new trip records through the admin application. The form submits trip data to the protected backend API using an authenticated request.

### Edit and Update Trip

Existing trip records can be edited and updated through the Angular interface. Updates are sent to the backend API using the trip code as the record identifier.

### Delete Trip

Administrators can delete trip records through the admin interface. Delete requests are sent to the protected backend API.

### Protected Routes

Administrative routes are protected with an Angular auth guard so that unauthenticated users cannot access trip management pages.

### API Service Layer

The application uses Angular services to separate API communication from component logic. This improves maintainability and keeps the application organized.

## Backend API Connection

The admin application was tested against the Travlr Getaways backend running locally at:

```text
http://localhost:3000
```

The Angular admin application runs locally at:

```text
http://localhost:4200
```

The Angular application communicates with the backend API through endpoints such as:

```text
http://localhost:3000/api
```

## Core API Workflows

The admin application uses the backend API to support the following workflows:

### Authentication

- `POST /api/login` — authenticate an administrator and receive a JWT token

### Trip Management

- `GET /api/trips` — retrieve all trips
- `GET /api/trips/:tripCode` — retrieve a single trip by code
- `POST /api/trips` — add a new trip
- `PUT /api/trips/:tripCode` — update an existing trip
- `DELETE /api/trips/:tripCode` — delete a trip

Protected requests require a valid bearer token in the `Authorization` header.

## Local Development

### Prerequisites

Before running the Angular admin application, make sure the backend project is running separately.

Required tools:

- Node.js
- npm
- Angular CLI
- Travlr Getaways backend API
- MongoDB connection used by the backend

### Install Dependencies

```bash
npm install
```

### Start the Angular Development Server

```bash
ng serve
```

Once the server is running, open the browser and navigate to:

```text
http://localhost:4200/
```

The application automatically reloads when source files are changed.

### Start the Backend API

The backend application should be started separately from the `travlr-express` project folder.

```bash
npm start
```

Backend URL:

```text
http://localhost:3000
```

## Building

To build the Angular project, run:

```bash
ng build
```

The build artifacts are stored in the `dist/` directory.

## Running Unit Tests

To execute unit tests with the configured test runner, use:

```bash
ng test
```

## Running End-to-End Tests

To run end-to-end tests, use:

```bash
ng e2e
```

Angular CLI does not include an end-to-end testing framework by default. One can be added depending on project requirements.

## Project Structure

Common Angular project areas include:

- `src/app/` — Angular application source code
- `src/app/components/` — application components
- `src/app/services/` — service classes for API and authentication logic
- `src/app/models/` — TypeScript models and interfaces
- `src/app/app.routes.ts` — application route configuration
- `src/main.ts` — Angular application bootstrap file
- `angular.json` — Angular workspace configuration
- `package.json` — project dependencies and scripts

## What This Project Demonstrates

This project demonstrates:

- Angular single-page application development
- Component-based front-end architecture
- TypeScript-based application logic
- Angular routing and navigation
- Form-based CRUD workflows
- REST API integration
- JWT authentication handling
- Protected route implementation using auth guards
- Separation of concerns through components, services, models, and routing
- Integration between an Angular front end and an Express/MongoDB backend
- Full stack administrative workflow testing

## Additional Resources

For more information about Angular CLI commands and Angular development, visit the Angular CLI documentation:

```text
https://angular.dev/tools/cli
```