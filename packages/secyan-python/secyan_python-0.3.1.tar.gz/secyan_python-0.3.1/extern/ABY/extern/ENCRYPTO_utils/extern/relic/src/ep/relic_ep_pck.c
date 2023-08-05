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
 * Implementation of point compression on prime elliptic curves.
 *
 * @ingroup ep
 */

#include "relic_core.h"

/*============================================================================*/
/* Public definitions                                                         */
/*============================================================================*/

void ep_pck(ep_t r, const ep_t p) {
	int b = fp_get_bit(p->y, 0);
	fp_copy(r->x, p->x);
	fp_zero(r->y);
	fp_set_bit(r->y, 0, b);
	fp_set_dig(r->z, 1);
	r->norm = 1;
}

int ep_upk(ep_t r, const ep_t p) {
	fp_t t;
	int result = 0;

	fp_null(t);

	TRY {
		fp_new(t);

		ep_rhs(t, p);

		/* t0 = sqrt(x1^3 + a * x1 + b). */
		result = fp_srt(t, t);

		if (result) {
			/* Verify if least significant bit of the result matches the
			 * compressed y-coordinate. */
			if (fp_get_bit(t, 0) != fp_get_bit(p->y, 0)) {
				fp_neg(t, t);
			}
			fp_copy(r->x, p->x);
			fp_copy(r->y, t);
			fp_set_dig(r->z, 1);
			r->norm = 1;
		}
	}
	CATCH_ANY {
		THROW(ERR_CAUGHT);
	}
	FINALLY {
		fp_free(t);
	}
	return result;
}
