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
 * Implementation of the library basic functions.
 *
 * @ingroup relic
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "relic_core.h"
#include "relic_rand.h"
#include "relic_types.h"
#include "relic_err.h"
#include "relic_arch.h"
#include "relic_fp.h"
#include "relic_fb.h"
#include "relic_ep.h"
#include "relic_eb.h"
#include "relic_cp.h"
#include "relic_pp.h"

/*============================================================================*/
/* Private definitions                                                        */
/*============================================================================*/

/** Error message respective to ERR_NO_MEMORY. */
#define MSG_NO_MEMORY 		"not enough memory"
/** Error message respective to ERR_PRECISION. */
#define MSG_NO_PRECI 		"insufficient precision"
/** Error message respective to ERR_NO FILE. */
#define MSG_NO_FILE			"file not found"
/** Error message respective to ERR_NO_READ. */
#define MSG_NO_READ			"can't read bytes from file"
/** Error message respective to ERR_NO_VALID. */
#define MSG_NO_VALID		"invalid value passed as input"
/** Error message respective to ERR_NO_BUFFER. */
#define MSG_NO_BUFFER		"insufficient buffer capacity"
/** Error message respective to ERR_NO_FIELD. */
#define MSG_NO_FIELD		"no finite field supported at this security level"
/** Error message respective to ERR_NO_CURVE. */
#define MSG_NO_CURVE		"no curve supported at this security level"
/** Error message respective to ERR_NO_CONFIG. */
#define MSG_NO_CONFIG		"invalid library configuration"

/*============================================================================*/
/* Public definitions                                                         */
/*============================================================================*/

/**
 * If multi-threading is enabled, assigns each thread a local copy of the data.
 */
#if MULTI == PTHREAD
#define thread 	__thread
#else
#define thread /* */
#endif

/**
 * Default library context.
 */
thread ctx_t first_ctx;

/**
 * Active library context.
 */
thread ctx_t *core_ctx = NULL;

#if MULTI == OPENMP
#pragma omp threadprivate(first_ctx, core_ctx)
#endif

int core_init(void) {
	if (core_ctx == NULL) {
		core_ctx = &(first_ctx);
	}

#ifdef CHECK
	core_ctx->reason[ERR_NO_MEMORY] = MSG_NO_MEMORY;
	core_ctx->reason[ERR_NO_PRECI] = MSG_NO_PRECI;
	core_ctx->reason[ERR_NO_FILE] = MSG_NO_FILE;
	core_ctx->reason[ERR_NO_READ] = MSG_NO_READ;
	core_ctx->reason[ERR_NO_VALID] = MSG_NO_VALID;
	core_ctx->reason[ERR_NO_BUFFER] = MSG_NO_BUFFER;
	core_ctx->reason[ERR_NO_FIELD] = MSG_NO_FIELD;
	core_ctx->reason[ERR_NO_CURVE] = MSG_NO_CURVE;
	core_ctx->reason[ERR_NO_CONFIG] = MSG_NO_CONFIG;
	core_ctx->last = NULL;
#endif /* CHECK */

#ifdef OVERH
	core_ctx->over = 0;
#endif

	core_ctx->code = RLC_OK;

	TRY {
		arch_init();
		rand_init();
#ifdef WITH_FP
		fp_prime_init();
#endif
#ifdef WITH_FB
		fb_poly_init();
#endif
#ifdef WITH_FT
		ft_poly_init();
#endif
#ifdef WITH_EP
		ep_curve_init();
#endif
#ifdef WITH_EB
		eb_curve_init();
#endif
#ifdef WITH_ED
		ed_curve_init();
#endif
#ifdef WITH_PP
		pp_map_init();
#endif
	}
	CATCH_ANY {
		return RLC_ERR;
	}

	return RLC_OK;
}

int core_clean(void) {
	rand_clean();
#ifdef WITH_FP
	fp_prime_clean();
#endif
#ifdef WITH_FB
	fb_poly_clean();
#endif
#ifdef WITH_FT
	ft_poly_clean();
#endif
#ifdef WITH_EP
	ep_curve_clean();
#endif
#ifdef WITH_EB
	eb_curve_clean();
#endif
#ifdef WITH_ED
	ed_curve_clean();
#endif
#ifdef WITH_PP
	pp_map_clean();
#endif
	arch_clean();
	core_ctx = NULL;
	return RLC_OK;
}

ctx_t *core_get(void) {
	return core_ctx;
}

void core_set(ctx_t *ctx) {
	core_ctx = ctx;
}
