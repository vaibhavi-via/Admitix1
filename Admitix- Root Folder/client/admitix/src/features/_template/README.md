# Feature module template

Copy this whole folder and rename it (`students`, `leads`, `jobs`, ...).
A finished module looks like:

```
features/
└── students/
    ├── pages/
    │   ├── ListPage.jsx
    │   ├── CreatePage.jsx
    │   ├── EditPage.jsx
    │   └── DetailsPage.jsx
    ├── components/
    │   ├── StudentForm.jsx
    │   ├── StudentTable.jsx
    │   └── StudentCard.jsx
    ├── services.js      # api calls, imports the shared axios instance
    ├── validation.js    # form validation rules
    └── constants.js      # module-specific constants (status options, etc.)
```

The List/Create/Edit/Details page pattern and the DataTable/Form component
pack ship in the next stage of the starter kit. Until then, build a simple
`services.js` + a page that lists your data, and wire it into `App.jsx`
and `Sidebar.jsx` as described in the root README.
