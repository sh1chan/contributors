v0.1.0
------
- [ ] Auth
- [ ] Projects
- [ ] Issues


## TODO Checkbox
### Database
- [ ] Tables
    - [ ] User
        - [ ] Filters
        - [ ] Issues    ;; @type {added, followed, voted}
        - [ ] Projects  ;; @type {added, followed, voted}
    - [ ] Issues
        - [ ] Tags
        - [ ] Labels
        - [ ] Votes     ;; Filter
    - [ ] Tags
    - [ ] Labels

### Routers
- [ ] Auth
    - [ ] /register
        - [ ] `GET`
        - [ ] `POST`
    - [ ] /login
        - [ ] `GET`
        - [ ] `POST`
    - [ ] /logoug
        - [ ] `POST`
    - [ ] /
    - [ ] /update
    - [ ] /delete
- [ ] Users
    - [ ] /
    - [ ] /{id}
- [ ] Teams
    - [ ] /
    - [ ] /create
    - [ ] /{id}
    - [ ] /{id}/update
    - [ ] /{id}/delete
- [ ] Projects
    - [ ] /
        - [ ] `GET`
    - [ ] /create
    - [ ] /{id}
    - [ ] /{id}/update
    - [ ] /{id}/delete
- [ ] Issues
    - [ ] /
        - [ ] `GET`
    - [ ] /create
    - [ ] /{id}
    - [ ] /{id}/update
    - [ ] /{id}/delete
    - [ ] /{id}/vote

### Schemas