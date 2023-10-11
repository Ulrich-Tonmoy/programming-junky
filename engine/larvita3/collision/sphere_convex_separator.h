//
// C++ Interface: sphere_convex_separator
//
// Description: 
//
//
// Author: Juan Linietsky <reduzio@gmail.com>, (C) 2007
//
// Copyright: See COPYING file that comes with this distribution
//
//
#ifndef SPHERE_CONVEX_SEPARATOR_H
#define SPHERE_CONVEX_SEPARATOR_H


#include "collision/volume_separator.h"

/**
 *	@author Juan Linietsky <reduzio@gmail.com>
 *
 *	This is a reference implementation. Will not be used if GJK is enabled.
*/

class SphereConvexSeparator : public VolumeSeparator {
public:

	virtual bool handles( const Volume& p_A, const Volume& p_B ) const;
	virtual void separate( const Volume& p_A,const Matrix4& p_A_transform, const Volume& p_B, const Matrix4 &p_B_transform, VolumeContactHandler *p_contact_handler) const;
};

#endif
