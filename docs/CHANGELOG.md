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