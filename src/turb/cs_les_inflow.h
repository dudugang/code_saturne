
#ifndef __CS_LES_INFLOW_H__
#define __CS_LES_INFLOW_H__

/*============================================================================
 * Turbulent inflow generation
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

/*----------------------------------------------------------------------------
 *  Local headers
 *----------------------------------------------------------------------------*/

#include "cs_base.h"

/*----------------------------------------------------------------------------*/

BEGIN_C_DECLS

/*============================================================================
 * Macro definitions
 *============================================================================*/

/*============================================================================
 * Type definitions
 *============================================================================*/

/*----------------------------------------------------------------------------
 * Type of synthetic turbulence generation
 *----------------------------------------------------------------------------*/

typedef enum {

  CS_INFLOW_LAMINAR,  /* Laminar fluctuations (i.e no fluctuation) */
  CS_INFLOW_RANDOM,   /* Gaussian random fluctuation */
  CS_INFLOW_BATTEN,   /* Fluctuations generated by the Batten method */
  CS_INFLOW_SEM       /* Fluctuations generated by the Synthetic Eddy Method */

} cs_inflow_type_t;

/*=============================================================================
 * Local Structure Definitions
 *============================================================================*/

/* Inlet definition */
/*------------------*/

typedef struct _cs_inlet_t  cs_inlet_t;

/*=============================================================================
 * Public function prototypes for Fortran API
 *============================================================================*/

/*----------------------------------------------------------------------------
 * Creation of a structure for the inlets
 *----------------------------------------------------------------------------*/

void CS_PROCF(defsyn, DEFSYN)
(
 cs_int_t            *n_inlets     /* <-- number of inlets                    */
);

/*----------------------------------------------------------------------------
 * General synthetic turbulence generation
 *----------------------------------------------------------------------------*/

void CS_PROCF(synthe, SYNTHE)(
 const cs_int_t  *const nvar,      /* --> number of variables                 */
 const cs_int_t  *const nscal,     /* --> number of scalars                   */
 const cs_int_t  *const iu,        /* --> index of velocity component         */
 const cs_int_t  *const iv,        /* --> index of velocity component         */
 const cs_int_t  *const iw,        /* --> index of velocity component         */
 const cs_real_t *const ttcabs,    /* --> current physical time               */
 const cs_real_t        dt[],      /* --> time step                           */
       cs_real_t        rcodcl[]   /* <-> boundary conditions array           */
);

void CS_PROCF(cs_user_les_inflow_init, CS_USER_LES_INFLOW_INIT)(
 cs_int_t              *nent       /* <-- number of LES inlets                */
);

void CS_PROCF(cs_user_les_inflow_define, CS_USER_LES_INFLOW_DEFINE)(
 const cs_int_t  *const nument,    /* --> id of the inlet                     */
          int         *typent,     /* <-- type of inflow method at the inlet  */
          int         *nelent,     /* <-- numb. of entities of the inflow meth*/
          int         *iverbo,     /* <-- verbosity level                     */
       cs_int_t       *nfbent,     /* <-- numb. of bound. faces of the inlet  */
       cs_int_t        lfbent[],   /* <-- list of bound. faces of the inlet   */
       cs_real_t       vitent[],   /* <-- ref. mean velocity at the inlet     */
       cs_real_t      *enrent,     /* <-- ref. turb. kin. ener. at the inlet  */
       cs_real_t      *dspent      /* <-- ref. turb. dissipation at the inlet */
);

void CS_PROCF(cs_user_les_inflow_advanced, CS_USER_LES_INFLOW_ADVANCED)(
 const cs_int_t  *const nument,    /* --> id of the inlet                     */
 const cs_int_t  *const nfbent,    /* --> numb. of bound. faces of the inlet  */
 const cs_int_t  *const nvar,      /* --> number of variables                 */
 const cs_int_t  *const nscal,     /* --> number of scalars                   */
 const cs_int_t         lfbent[],  /* --> list of bound. faces of the inlet   */
 const cs_real_t        dt[],      /* --> time step                           */
       cs_real_t        uent[],    /* <-- mean velocity at the inlet faces    */
       cs_real_t        rijent[],  /* <-- turb. kin. ener. at the inlet faces */
       cs_real_t        epsent[]   /* <-- turb. dissipation at the inlet faces*/
);

/*----------------------------------------------------------------------------
 * Read the restart file of the LES inflow module
 *----------------------------------------------------------------------------*/

void CS_PROCF(lecsyn, LECSYN)
(
 const char  *filename
);

/*----------------------------------------------------------------------------
 * Write the restart file of the LES inflow module
 *----------------------------------------------------------------------------*/

void CS_PROCF(ecrsyn, ECRSYN)
(
 const char  *filename
);

/*=============================================================================
 * Public function prototypes
 *============================================================================*/

/*----------------------------------------------------------------------------
 * Finalize turbulent inflow generation API.
 *----------------------------------------------------------------------------*/

void
cs_inflow_finalize(void);

/*----------------------------------------------------------------------------*/

END_C_DECLS

#endif /* __CS_LES_INFLOW_H__ */
