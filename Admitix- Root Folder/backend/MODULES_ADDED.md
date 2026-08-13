# Added modules

The following standalone CRUD modules have been added and registered in
`app/router.py`:

- `staff` — `/staff`
- `educational_details` — `/educational-details`
- `entrance_exam_scores` — `/entrance-exam-scores`
- `application_preferences` — `/application-preferences`

They reuse the project's existing ORM entities and database tables, so no data
migration is required. Each module provides model access, Pydantic schemas,
router, service, repository, dependency, permissions, validation, constants,
and exception files.
