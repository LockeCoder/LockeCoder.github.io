# Travlr Getaways — Express API (CS 499 enhanced version)

This source folder contains the customer-facing Express/Handlebars application, MongoDB models, public trip listing and the administrator-protected trip API. The matching Angular administrator application is part of the same capstone artifact.

## Setup

1. Install Node.js and MongoDB and start the MongoDB service.
2. In this directory run `npm install`. This will create the dependency lockfile because the archived milestone lockfile lacked `mongoose` and was not valid for the revised dependency list.
3. Configure `JWT_SECRET` to a **random value of at least 32 characters**; do not use the example file as a real secret. Optionally set `MONGO_URI` (default `mongodb://127.0.0.1/travlr`). Do not commit local `.env` files. Node does not automatically load `.env`; export the variables in your shell or use a trusted environment loader.
4. To create the first administrator, set `ADMIN_NAME`, `ADMIN_EMAIL` and `ADMIN_PASSWORD` (at least 12 characters) as environment variables. Run `npm run setup:admin`. Remove `ADMIN_PASSWORD` from the environment afterward.
5. Run `npm start` for the API and website. The Angular SPA connects to the API on `http://localhost:3000/api` by default.
6. Run `npm test` for dependency-free configuration tests. Full integration and Angular tests require installed dependencies and an available MongoDB instance.

## Security measures

- Public registration was disabled. Administrator accounts are provisioned offline and must have an `admin` role. Existing accounts without that role cannot authenticate as administrators.
- Only JWTs signed using the explicitly configured secret, verified under HS256, containing the administrator role and a user identifier are accepted for write operations. Tokens expire after two hours.
- New passwords are hashed with PBKDF2-HMAC-SHA512, 210,000 iterations, using a random salt. Legacy hashes remain recognizable for controlled migration of authorized administrator accounts, but legacy accounts lacking an administrator role require manual review.
- The browser-side route guard is only a UI convenience; the Express API enforces access rights.

## Portfolio release notes

This is a cleaned, revised educational artifact. No production security certification or fully passing application build is claimed. Dependencies could not be installed and full system tests could not be performed during this preparation. Review API authentication, role provisioning, CORS policy, package advisories and integration tests before any deployment. The original milestone submission remains unchanged.
