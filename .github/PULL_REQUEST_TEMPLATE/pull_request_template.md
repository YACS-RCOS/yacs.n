**Issue**

Note which issue number(s) this Pull Request closes. All pull requests should close an issue, if one does not exists, make one. This helps us plan and discuss before we decide on implementation

*Example:*
> closes #113

**Database Changes/Migrations**

If you added/modified a table, notify people of schema change here

*Example:*
> Added table `account_semester_selection` for a mapping from a students account and semester to a class and section (aka class/section selections)

**Test Modifications**

Note added unit/integration tests: (all backend changes should contain unit/integration tests with pytest)

*Example:*
> Added test `tests/api/db/test_classinfo.py:test_crn_uniqueness` to ensure all classes returned from API call don't have repeat CRNs

**Test Procedure**

Show procedure to test functionality with a clear procedure

*Example:*
> 1. Create a branch
> 2. Commit a change to that branch
> 3. Push branch
> 4. Create Pull Request and fill in PR template

**Photos**

Show before and after, capture screenshot/gif of finished feature/bug

**Additional Info**

More info that would help people review your change
