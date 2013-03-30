/*
 * chphostname.c
 * 
 * Pretty Hostname Changer - Changes Pretty Hostname of System
 *  Directly modifies /etc/machine-info file (if there is not, creates it)
 *  Same job can easily done by adding PRETTY_HOSTNAME=[NAME] line into
 *  file.
 * 
 * Static Hostname can be change by "hostnamectl set-hostname [NAME]"
 *  command via terminal (at least for Fedora 18)
 * 
 * Copyright 2013 Mehmet Akif TAŞOVA <makiftasova@gmail.com>
 * 
 * This program is free software; you can redistribute it and/or modify it 
 * under the terms of the GNU General Public License version 3 as published 
 * by the Free Software Foundation
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define EXIT_NONROOT 1

#define EXIT_ILLEGAL_ARGS 2

void usage(const char* execName);

int main(int argc, char** argv) {

    int uid = -1;
    FILE* outFilePtr;

    uid = getuid();

    if (0 != uid) {
        printf("Root permissions required for this operation.\n");
        return (EXIT_NONROOT);
    }

    if (argc != 2) {
        usage(argv[0]);
        return (EXIT_ILLEGAL_ARGS);
    }

    outFilePtr = fopen("/etc/machine-info", "w");
    fprintf(outFilePtr, "PRETTY_HOSTNAME=%s\n", argv[1]);
    fclose(outFilePtr);

    return (EXIT_SUCCESS);
}

void usage(const char* execName) {
    printf("Usage:\n------\n");
    printf("%s [NAME]\n", execName);
    return;
}

/* End of chphostname.c */
