#ifndef __CS_LAGR_HEAD_LOSSES_H__
#define __CS_LAGR_HEAD_LOSSES_H__

/*============================================================================
 * Functions and types for head losses and porosity
 *============================================================================*/

/*
  This file is part of Code_Saturne, a general-purpose CFD tool.

  Copyright (C) 1998-2018 EDF S.A.

  This program is free software; you can redistribute it and/or modify it under
  the terms of the GNU General Public License as published by the Free Software
  Foundation; either version 2 of the License, or (at your option) any later
  version.

  This program is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
  details.

  You should have received a copy of the GNU General Public License along with
  this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
  Street, Fifth Floor, Boston, MA 02110-1301, USA.
*/

/*----------------------------------------------------------------------------*/

#include "cs_defs.h"

/*----------------------------------------------------------------------------*/

BEGIN_C_DECLS

/*=============================================================================
 * Macro definitions
 *============================================================================*/

/*============================================================================
 * Type definitions
 *============================================================================*/

/*=============================================================================
 * Global variables
 *============================================================================*/

/*=============================================================================
 * Public function prototypes
 *============================================================================*/

/*----------------------------------------------------------------------------*/
/*!
 * \brief Define Head losses to take into account deposit in the flow
 */
/*----------------------------------------------------------------------------*/

void
CS_PROCF(laghlo, LAGHLO)(cs_lnum_t *ncepdc,
                         cs_lnum_t *icepdc,
                         cs_lnum_t  itypfb[],
                         cs_real_t  ckupdc[]);

/*----------------------------------------------------------------------------*/

END_C_DECLS

#endif /* __CS_LAGR_HEAD_LOSSES_H__ */
