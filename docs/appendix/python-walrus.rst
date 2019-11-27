
PEP 572 and The Walrus operator
===============================


.. code-block:: c

    #include <stdio.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>
    #include <string.h>
    #include <errno.h>

    int main(int argc, char *argv[]) {
        int rc = -1;
        struct stat *st = NULL;

        rc = stat("file-not-exist.txt", st);
        if (rc == -1) {
            fprintf(stderr, "stat file got error: %s", strerror(errno));
            goto end;
        }
        rc = 0;
    end:
        return rc;
    }


.. code-block:: c

    #include <stdio.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>
    #include <string.h>
    #include <errno.h>

    int main(int argc, char *argv[]) {
        int rc = -1;
        struct stat *st = NULL;

        // Yoda conditions + inline assignments
        if (-1 == (rc = stat("file-not-exist.txt", st))) {
            fprintf(stderr, "stat file got error: %s", strerror(errno));
            goto end;
        }
        rc = 0;
    end:
        return rc;
    }
