- [x] 15.11.2025
    ;; /issues/update/`GET`
    - [x] QueryParams
        - [x] `error_message`
    - [x] Redirect
        - [x] on premmision error
            - [x] router `issues_get`
        - [x] Add `error_message`
    - [x] Render Template
        - [x] `error_message`
    ;; /issues/update/`GET`
    - [x] Redirect
        - [x] on premmision error
            - [x] router `issues_get`
        - [x] on validation error
            - [x] router `get_issues_update`
        - [x] on success
            - [x] router `get_issues_update`
        - [x] Add `error_message`

- [x] 15.11.2025
    ;; /issues/update/`POST`
    - [x] User Required
    - [x] Validate form fields
        - [x] !Title
        - [x] !Tags
        - [x] Issues URL
            - [x] Github
                - [x] by netloc
                - [ ] by path
            - [ ] Gitlab
    - [x] Redirect user to the `issues_get` router
        - [x] Add `error_message`
    - [x] Remove `issue.id` from categories
    - [x] Add tags to the database
    - [x] Add labels to the database

- [x] 13.11.2025
    ;; /issues/create/`GET`
    - [x] Rename routers `new` to `create`
    ;; /issues/create/`POST`
    - [x] Rename routers `new` to `create`
    - [x] Update schemas `IssuesNewIn`

- [x] 11.11.2025
    ;; /issues/`GET`
    - [x] Render Template
        - [x] Actions
            - [x] Update link
    ;; /update/{issue_id}/`GET`
    - [x] User Required
    - [x] Issue Required
    - [x] Permissions Required
        - [x] IsOwner
    - [x] Render template
        - [x] New Issues Form

- [x] 09.11.2025
    ;; /issues/`GET`
    - [x] Render Template
        - [x] Actions
            - [x] Delete link
    ;; /issues/delete/{issue_id}/`GET`
    - [x] User Required
    - [x] Permissions Required
        - [x] User is a creator
            - [x] orelse Redirect user to the `issues_get` router
                - [x] Erorr messages
    - [x] Render Template
        - [x] User Required
        - [x] Issue Form
            - [x] post to `post_issues_delete`
    ;; /issues/delete/{issue_id}/`POST`
    - [x] User Required
    - [x] Permissions Required
        - [x] User is a creator
            - [x] orelse Redirect user to the `issues_get` router
                - [x] Erorr messages

- [x] 08.11.2025
    ;; /issues/`GET`
    - [x] Filter Issues
        - [x] Id
        - [x] createdBy
    - [x] Render Template
        - [x] `issues.id`
        - [x] `issues.created_by`
    ;; /issues/new/`POST`
    - [x] Remove tables `issues` fields `added_by`

- [x] 07.11.2025
    ;; /issues/`GET`
    - [x] Filter Issues
        - [x] title
        - [x] tags
        - [x] labels
    ;; /issues/`POST`
    - [x] Save user filters
    - [x] Redirect user to the `issues_get` router
    ;; /issues/new/`POST`
    - [x] Add tags to the database
    - [x] Add labels to the database