# Test data

These files allow for some integration testing.
All files in [`resumes`](resumes/) are expected to have a corresponding output file in [`expected-outputs`](expected-outputs/).
The reverse is **not** true:

- the `showcase.resume.json` needs to be part of the application, not test data and is therefore tested differently (it still has an expected output file)
