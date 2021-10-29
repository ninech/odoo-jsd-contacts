# Jira Service Desk Contact Sync

Our Odoo to Jira Service Desk contact data sync module.

```sh
docker-compose up -d db
docker-compose up odoo
```

Username and password are `admin` and `admin`.

## Tests

Run tests with the following command:

```sh
/entrypoint.sh -d odoo -u jsd_contacts --test-enable --log-level test --stop-after-init
```
