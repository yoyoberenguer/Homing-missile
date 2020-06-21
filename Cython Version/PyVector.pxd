
# --------------- C DECLARATION ----------------
cdef extern from 'vector.c':

    struct vector2d:
       float x;
       float y;
# ----------------------------------------------


cpdef vector2d v_vector2d(float x, float y)

cpdef vector2d v_sub_inplace(vector2d v1, vector2d v2)
 
cpdef vector2d v_add_inplace(vector2d v1, vector2d v2)

cpdef float v_length(vector2d v)
  
cpdef float v_distance_to(vector2d v1, vector2d v2)

cpdef vector2d v_init(vector2d v, float x, float y)

cpdef vector2d v_add_components(vector2d v1, vector2d v2)
    
cpdef vector2d v_sub_components(vector2d v1, vector2d v2)

cpdef void v_scale_inplace(float c, vector2d v)

cpdef float v_dot(vector2d v1, vector2d v2)

cpdef float v_distance_squared_to(vector2d v1, vector2d v2)

cpdef vector2d v_div_inplace(vector2d v1, vector2d v2)

cpdef vector2d v_mul_inplace(vector2d v1, vector2d v2)

cpdef vector2d v_mul_components(vector2d v1, vector2d v2)

cpdef vector2d v_div_components(vector2d v1, vector2d v2)
    
cpdef vector2d v_normalize (vector2d v)

cpdef vector2d v_scale_to_length(vector2d v, float c)

cpdef float v_length_squared(vector2d v)

cpdef vector2d v_rotate_deg(vector2d v, float deg)

cpdef vector2d v_rotate_rad(vector2d v, float rad)

cpdef float v_angle_to(vector2d v1, vector2d v2)

cpdef float v_angle_rad(vector2d v)

cpdef float v_angle_deg(vector2d v)

cpdef vector2d angle_vector(vector2d player, vector2d rect, vector2d speed)

cpdef vector2d rand_angle(int minimum, int maximum, float angle)

cpdef vector2d rand_angle_inplace(vector2d v, int minimum, int maximum, float angle)

cpdef vector2d rand_angle_f(float minimum, float maximum, float angle)

cpdef vector2d rand_angle_inplacef(vector2d v, float minimum, float maximum, float angle)

