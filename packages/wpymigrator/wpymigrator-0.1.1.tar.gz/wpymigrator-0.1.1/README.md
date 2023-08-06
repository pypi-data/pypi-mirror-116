# WPyMigrator

A program designed to aide in WordPress development site creation, and integration back into production.

---

## Non-python dependencies

Currently planning to utilize WP-cli.
This may be removed at a later date.
You can verify it is installed with the following command:

```bash
$ wp --version
# Expected output: WP-CLI x.x.x
```

If not installed:
```bash
$ curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
$ chmod +x wp-cli.phar
$ sudo mv wp-cli.phar /usr/local/bin/wp
$ wp --version
# Expected output: WP-CLI x.x.x
```
