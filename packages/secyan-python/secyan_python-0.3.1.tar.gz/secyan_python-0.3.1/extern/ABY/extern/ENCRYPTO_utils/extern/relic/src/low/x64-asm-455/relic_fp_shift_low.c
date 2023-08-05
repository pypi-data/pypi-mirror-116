/*
 * RELIC is an Efficient LIbrary for Cryptography
 * Copyright (C) 2007-2019 RELIC Authors
 *
 * This file is part of RELIC. RELIC is legal property of its developers,
 * whose names are not listed here. Please refer to the COPYRIGHT file
 * for contact information.
 *
 * RELIC is free software; you can redistribute it and/or modify it under the
 * terms of the version 2.1 (or later) of the GNU Lesser General Public License
 * as published by the Free Software Foundation; or version 2.0 of the Apache
 * License as published by the Apache Software Foundation. See the LICENSE files
 * for more details.
 *
 * RELIC is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 * A PARTICULAR PURPOSE. See the LICENSE files for more details.
 *
 * You should have received a copy of the GNU Lesser General Public or the
 * Apache License along with RELIC. If not, see <https://www.gnu.org/licenses/>
 * or <https://www.apache.org/licenses/>.
 */

/**
 * @file
 *
 * Implementation of the low-level prime field shifting functions.
 *
 * @ingroup bn
 */

#include <gmp.h>

#include "relic_fp.h"
#include "relic_fp_low.h"

/*============================================================================*/
/* Public definitions                                                         */
/*============================================================================*/

dig_t fp_lsh1_low(dig_t *c, const dig_t *a) {
	return mpn_lshift(c, a, RLC_FP_DIGS, 1);
}

dig_t fp_lshb_low(dig_t *c, const dig_t *a, int bits) {
	return mpn_lshift(c, a, RLC_FP_DIGS, bits);
}

void fp_lshd_low(dig_t *c, const dig_t *a, int digits) {
	dig_t *top;
	const dig_t *bot;
	int i;

	top = c + RLC_FP_DIGS - 1;
	bot = a + RLC_FP_DIGS - 1 - digits;

	for (i = 0; i < RLC_FP_DIGS - digits; i++, top--, bot--) {
		*top = *bot;
	}
	for (i = 0; i < digits; i++, c++) {
		*c = 0;
	}
}

dig_t fp_rshb_low(dig_t *c, const dig_t *a, int bits) {
	return mpn_rshift(c, a, RLC_FP_DIGS, bits);
}

void fp_rshd_low(dig_t *c, const dig_t *a, int digits) {
	const dig_t *top;
	dig_t *bot;
	int i;

	top = a + digits;
	bot = c;

	for (i = 0; i < RLC_FP_DIGS - digits; i++, top++, bot++) {
		*bot = *top;
	}
	for (; i < RLC_FP_DIGS; i++, bot++) {
		*bot = 0;
	}
}
