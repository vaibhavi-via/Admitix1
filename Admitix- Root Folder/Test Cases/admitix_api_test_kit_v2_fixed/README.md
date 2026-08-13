# Admitix API Test Kit v2 — Fixed

This is the corrected v2 tester. The previous v2 package had a missing
exception handler in the GET loop, which caused a SyntaxError.

Run:

```bat
py test_all_apis.py
```

Optional authentication:

```bat
set ADMITIX_EMAIL=your@email.com
set ADMITIX_PASSWORD=yourpassword
py test_all_apis.py
```

This version is non-destructive: it only performs health, OpenAPI,
authentication (when supplied), and GET/detail GET tests. It does not
POST, PATCH, or DELETE anything.
