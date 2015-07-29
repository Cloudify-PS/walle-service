===============================
Score {version} release process
===============================

{version} name
{version} source branch URL
{version} description
{version} release date
{version} authors:

# See: git log --format='%aN <%aE>' | awk '{arr[$0]++} END{for (i in arr){print arr[i], i;}}' | sort -rn | cut -d\  -f2-


ChangeLog for {version}
=======================

{Change log}

# See: git log --oneline --decorate {version}..

Components for Score {version}
==============================

{Components for Score {version}}


Requirements for Score {version}
================================

Common stack
------------

{common stack}

Cloudify stack
--------------

{cloudify stack}


Testing requirements for Score {version}
========================================


External dependencies/requirements for Score {version}
======================================================

VMware stack
------------

{vmware stack}

Cloudify stack
--------------

{cloudify stack}

================
Approved plugins
================

{approved plugins}

========
Security
========

{security section}
