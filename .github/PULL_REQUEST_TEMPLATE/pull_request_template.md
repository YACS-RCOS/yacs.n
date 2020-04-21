**Related Issues**

Note which issue number(s) this Pull Request closes

*Example:*
> closes #113

**Database Changes/Migrations**

If you added/modified a table, notify people of schema change here

*Example:*
> Added table `account_semester_selection` for a mapping from a students account and semester to a class and section (aka class/section selections)

**Added/Altered API Routes***

List added/altered API Routes

*Example:*
> Added: `GET /api/class/FALL-2020` - Fetch all classes from semester (Fall-2020)
> 
> Modified: `GET /api/class/FALL-2020?meet-prerequisites=true` - Added filtering on prerequistite through query string

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
