## E2E Tests for APEL and FTS

These tests form part of the end-to-end testing platform for APEL Accounting and File Transfer Service (FTS).
The platform allows grid jobs and data transfer submissions to be traced from start to finish, ensuring correct
functionality and successful execution of both services.

Tests include:

APEL: successful grid job submission, and then the query of an accounting `supersummary` from the APEL DB,
to ensure data successfully propagated along the accounting pipeline.

FTS: Successful file transfer submission to `ska` (via token authentication), and `wlcg` and `test` (via
certificate authentication) FTS endpoints. Then performing an HTTP request to retrieve the transfer
information, checking the file transfer completed as expected.

The test results are displayed in an OpenSearch dashboard (currently only pre-production) which can be found at:
https://stephano-dashboards.scd.stfc.ac.uk/app/dashboards#/view/336d7730-e1dd-11f1-9904-b307b026ae08


### To run the E2E tests:
There is a deployment script and configuration files on Aquilon, under the
`ral-tier1/features/monitoring/fed-services-e2e` directory. Or you can access it at:
https://phabricator.gridpp.rl.ac.uk/diffusion/AQ/browse/prod/ral-tier1/features/monitoring/fed-services-e2e/ .
These scripts clone this repository onto a VM.

The script should set up two log files. These should get ingested by the Logstash/Filebeat configuration (on
Aquilon) and sent to the OpenSearch dashboard.

The test runner and the apel db querier get triggered daily by a systemd timer, with the results written to the
logfiles.

The VM these tests are run on needs to be able to run grid jobs and FTS transfers, have access to the APEL
database, and have web access.
