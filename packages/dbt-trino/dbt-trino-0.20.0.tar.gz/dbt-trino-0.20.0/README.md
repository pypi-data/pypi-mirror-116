## dbt-trino

### Introduction

One frequently asked question in the context of using `dbt` tool is:

> Can I connect my dbt project to two databases?

(see the answered [question](https://docs.getdbt.com/faqs/connecting-to-two-dbs-not-allowed) on the dbt website).

**tldr;** `dbt` stands for transformation as in `T` within `ELT`  pipelines, it doesn't move data from source to a warehouse.

The creators of the `dbt` tool have added however support for handling such scenarios via
[dbt-presto](https://github.com/dbt-labs/dbt-presto) plugin.

This repository represents a fork of the [dbt-presto](https://github.com/dbt-labs/dbt-presto) with slight
adaptations to make it work with [Trino](https://trino.io/) SQL compute engine.

### Compatibility

This dbt plugin has been tested against `dbt` version `0.20.0` and `trino`  version `359`.

### Installation

This dbt adapter can be installed via pip:

```
$ pip install dbt-trino
```

### Configuring your profile

A dbt profile can be configured to run against Trino using the following configuration:

| Option  | Description                                        | Required?               | Example                  |
|---------|----------------------------------------------------|-------------------------|--------------------------|
| method  | The Trino authentication method to use | Optional (default is `none`)  | `none` or `kerberos` |
| user  | Username for authentication | Required  | `commander` |
| password  | Password for authentication | Optional (required if `method` is `ldap` or `kerberos`)  | `none` or `abc123` |
| database  | Specify the database to build models into | Required  | `analytics` |
| schema  | Specify the schema to build models into. Note: it is not recommended to use upper or mixed case schema names | Required | `public` |
| host    | The hostname to connect to | Required | `127.0.0.1`  |
| port    | The port to connect to the host on | Required | `8080` |
| threads    | How many threads dbt should use | Optional (default is `1`) | `8` |



**Example profiles.yml entry:**
```
my-trino-db:
  target: dev
  outputs:
    dev:
      type: trino
      user: commander
      host: 127.0.0.1
      port: 8080
      database: analytics
      schema: public
      threads: 8
```

### Usage Notes

#### Supported Functionality
Due to the nature of Trino, not all core `dbt` functionality is supported.
The following features of dbt are not implemented on Trino:
- Archival
- Incremental models

Also, note that upper or mixed case schema names will cause catalog queries to fail. 
Please only use lower case schema names with this adapter.


#### Required configuration
dbt fundamentally works by dropping and creating tables and views in databases.
As such, the following Trino configs must be set for dbt to work properly on Trino:

```
hive.metastore-cache-ttl=0s
hive.metastore-refresh-interval = 5s
hive.allow-drop-table=true
hive.allow-rename-table=true
```



### Running tests
Build dbt container locally:

```
./docker/dbt/build.sh
```

Run a Trino server locally:

```
./docker/init.bash
```

If you see errors while about "inconsistent state" while bringing up Trino,
you may need to drop and re-create the `public` schema in the hive metastore:
```
# Example error

Initialization script hive-schema-2.3.0.postgres.sql
Error: ERROR: relation "BUCKETING_COLS" already exists (state=42P07,code=0)
org.apache.hadoop.hive.metastore.HiveMetaException: Schema initialization FAILED! Metastore state would be inconsistent !!
Underlying cause: java.io.IOException : Schema script failed, errorcode 2
Use --verbose for detailed stacktrace.
*** schemaTool failed ***
```

**Solution:** Drop (or rename) the public schema to allow the init script to recreate the metastore from scratch. **Only run this against a test Trino deployment. Do not run this in production!**
```sql
-- run this against the hive metastore (port forwarded to 10005 by default)
-- DO NOT RUN THIS IN PRODUCTION!

drop schema public cascade;
create schema public;
```

You probably should be slightly less reckless than this.

Run tests against Trino:

```
./docker/run_tests.bash
```

Run the locally-built docker image (from docker/dbt/build.sh):
```
export DBT_PROJECT_DIR=$HOME/... # wherever the dbt project you want to run is
docker run -it --mount "type=bind,source=$HOME/.dbt/,target=/home/dbt_user/.dbt" --mount="type=bind,source=$DBT_PROJECT_DIR,target=/usr/app" --network dbt-net dbt-trino /bin/bash
```

### Running integration tests

Install [dbt-adapter-tests](https://github.com/dbt-labs/dbt-adapter-tests) library to be able to run the dbt tests:

```
pip install pytest-dbt-adapter
```

Run from the base directory of the project the command:

```
pytest test/integration/trino.dbtspec
```

## Code of Conduct

Everyone interacting in the dbt project's codebases, issue trackers, chat rooms, and mailing lists is expected 
to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).
