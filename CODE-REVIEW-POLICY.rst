================================================
Code reviewing, Submission, Acceptance policies.
================================================

----------
Committing
----------

Commit message must contain::

    * Detailed content of the work done on the patch.
    * In order to run real-mode integration tests ,as part of CI checks,
      over submitted pull request each developer should explicitly mention
      specific flag inside commit message  body:
             RunIntegrationTests: True
      Otherwise, pull request will be tested with fake-mode integration tests
      (including fake vCloud and Cloudify manager).


----------
Submitting
----------

In order to keep code quality at highest level as developers we MUST think of next points during proposing code::

    * Feature design was approved by the development team
    * If so, it is more than necessary to write tests (unit tests, integration tests, functional tests)
    * If you think that code is ready to be merged - ask other developers to review it.

--------------
Code accepting
--------------

Walle project follows next code accepting rules::

    * TWO +1's are required from other developers, excluding committee

---------
Reviewing
---------

This is a checklist that Good Code reviewer should follow, this is by no means complete, or suitable for everyone.

The golden rules::

    Good quality code reviews produce good quality code.

    Don’t be biased, treat colleagues (from the same company)
    the same as you would anyone else; or better yet, review their patches even harder.

    Avoid rubber stamping. Rubber stamping is +1’ing with no comments.
    Obviously this depends on the patch, if it’s a simple fix then it’s probably fine.
    But try to let the author know you’ve actually read and understood the changes,
    leave an inline comment or general comment.


If you are placing +1 to any of patches you are taking responsibility for its state, meaning::

    Code does work.

    Code passes all checks.

    If there a need of manual testing - please do it.

    If patch represents a new feature (new API, new service, refactored workflow, etc.)
    please take time to verify/test code.



The commit message::

    It goes title (on one line), then description (many lines).

    The title should be a summary of what’s happening: “Do x y z”.

    The description should explain WHY. Is the change a refactoring? Is it a bug?

    A new feature? What’s the motivation behind the change? It might be complicated, but it should be clear.

Know the keywords and their syntax::

    SCOR-xxxx
    Is there an APIImpact or SecurityImpact?


The Walle project encourages the guidelines (below)

A rating of +1 on a code review is indicated if::

     * It is your opinion that the change, as proposed, should be
       considered for merging.


A rating of 0 on a code review is indicated if::

     * The reason why you believe that the proposed change needs
       improvement is merely an opinion,

     * You have a question, or need a clarification from the author,

     * The proposed change is functional but you believe that there is
       a different, better, or more appropriate way in which to
       achieve the end result being sought by the proposed change,

     * There is an issue of some kind with the Commit Message,
       including violations of the Commit Message guidelines,

     * There is a typographical or formatting error in the commit
       message or the body of the change itself,

     * There could be improvements in the test cases provided as part
       of the proposed change.


A rating of -1 on a code review is indicated if::

     * The reason why you believe that the proposed change needs
       improvement is irrefutable, or it is a widely shared opinion as
       indicated by a number of +0 comments,

     * The subject matter of the change (not the commit message)
       violates some well understood OpenStack procedure(s),

     * The change contains content that is demonstrably inappropriate,

     * The test cases do not exercise the change(s) being proposed.

