#include <linux/prctl.h>
#include <sys/prctl.h>
#include <cap-ng.h>
#include <stdio.h>
#include <stdlib.h>

static void set_ambient_cap(int cap) {
	int rc;

	capng_get_caps_process();
	rc = capng_update(CAPNG_ADD, CAPNG_INHERITABLE, cap);
	if (rc) {
		printf("Cannot add inheritable cap\n");
		exit(2);
	}
	capng_apply(CAPNG_SELECT_CAPS);

	/* Note the two 0s at the end. Kernel checks for these */
	if (prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_RAISE, cap, 0, 0)) {
		perror("Cannot set cap");
		exit(1);
	}
}


int main(int argc, char **argv) {
	set_ambient_cap(CAP_DAC_READ_SEARCH);

	argv[0] = "/usr/bin/restic";
	if (execv("/usr/bin/restic", argv))
		perror("Cannot exec");

	return 0;
}
